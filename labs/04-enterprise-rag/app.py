from __future__ import annotations

import argparse
import json
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TOKEN_RE = re.compile(r"[\w\u4e00-\u9fff]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    """教学用 tokenizer：中文按连续片段切分，真实项目应替换为检索引擎自身 analyzer。"""
    return [token.lower() for token in TOKEN_RE.findall(text)]


@dataclass(frozen=True)
class Document:
    document_id: str
    tenant_id: str
    department: str
    title: str
    content: str


@dataclass(frozen=True)
class Evidence:
    document_id: str
    title: str
    content: str
    score: float


class DocumentStore:
    def __init__(self, path: Path) -> None:
        self.documents = self._load(path)

    @staticmethod
    def _load(path: Path) -> list[Document]:
        items: list[Document] = []
        with path.open("r", encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    items.append(Document(**json.loads(line)))
        return items

    def visible_to(self, tenant_id: str, department: str | None = None) -> list[Document]:
        # 企业 RAG 的权限过滤必须发生在召回之前，而不是回答生成之后。
        return [
            doc
            for doc in self.documents
            if doc.tenant_id == tenant_id
            and (department is None or doc.department == department)
        ]


class Retriever:
    """可替换的本地 Retrieval Baseline。

    真实项目可以替换成 pgvector / Qdrant / Elasticsearch，调用方无需改变。
    """

    def search(self, query: str, documents: Iterable[Document], top_k: int = 5) -> list[Evidence]:
        query_tokens = tokenize(query)
        query_set = set(query_tokens)
        candidates: list[Evidence] = []

        for doc in documents:
            haystack = f"{doc.title} {doc.content}"
            doc_tokens = tokenize(haystack)
            doc_set = set(doc_tokens)
            overlap = len(query_set & doc_set)

            # 给包含完整 Query 子串的候选额外 bonus，模拟 lexical retrieval 中的 phrase boost。
            phrase_bonus = 2.0 if query.lower() in haystack.lower() else 0.0
            length_norm = 1.0 / math.sqrt(max(len(doc_tokens), 1))
            score = overlap * length_norm + phrase_bonus

            if score > 0:
                candidates.append(
                    Evidence(
                        document_id=doc.document_id,
                        title=doc.title,
                        content=doc.content,
                        score=score,
                    )
                )

        candidates.sort(key=lambda item: item.score, reverse=True)
        return candidates[:top_k]


class Reranker:
    def rerank(self, query: str, candidates: list[Evidence], top_n: int = 3) -> list[Evidence]:
        # 教学用 deterministic reranker：实际项目可替换 cross-encoder / rerank API。
        query_chars = set(query.replace(" ", ""))

        def score(item: Evidence) -> float:
            text_chars = set((item.title + item.content).replace(" ", ""))
            char_overlap = len(query_chars & text_chars) / max(len(query_chars), 1)
            return item.score + char_overlap

        reranked = sorted(candidates, key=score, reverse=True)
        return reranked[:top_n]


class CitationBuilder:
    @staticmethod
    def build(evidence: list[Evidence]) -> list[dict[str, str]]:
        return [
            {
                "document_id": item.document_id,
                "title": item.title,
                "quote": item.content[:120],
            }
            for item in evidence
        ]


def answer(query: str, evidence: list[Evidence]) -> dict[str, object]:
    if not evidence:
        return {
            "status": "evidence_insufficient",
            "answer": "当前授权知识范围内没有足够证据支持该问题。",
            "citations": [],
        }

    # 为了让实验无需模型 API 即可运行，这里只做 Evidence 摘要拼接。
    # 接真实 LLM 时，应把 evidence 作为受控上下文，并要求答案引用 document_id。
    summary = "；".join(item.content for item in evidence)
    return {
        "status": "ok",
        "answer": f"基于当前证据：{summary}",
        "citations": CitationBuilder.build(evidence),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tenant", default="tenant-a")
    parser.add_argument("--query", default="供应商交付异常")
    parser.add_argument("--department", default=None)
    args = parser.parse_args()

    store = DocumentStore(Path(__file__).with_name("documents.jsonl"))
    visible_docs = store.visible_to(args.tenant, args.department)

    retriever = Retriever()
    reranker = Reranker()
    candidates = retriever.search(args.query, visible_docs)
    evidence = reranker.rerank(args.query, candidates)
    result = answer(args.query, evidence)

    print(json.dumps(
        {
            "tenant": args.tenant,
            "query": args.query,
            "visible_document_ids": [doc.document_id for doc in visible_docs],
            "retrieved_document_ids": [item.document_id for item in evidence],
            **result,
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
