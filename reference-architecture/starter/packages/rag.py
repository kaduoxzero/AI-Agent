from __future__ import annotations

from dataclasses import dataclass

from packages.contracts import Evidence


@dataclass(frozen=True)
class KnowledgeDocument:
    document_id: str
    tenant_id: str
    content: str


class ReferenceRetriever:
    """Small ACL-first retriever used by the starter.

    The important boundary is the interface and tenant filter. Replace the local
    corpus with pgvector / Elasticsearch / a managed vector database later.
    """

    def __init__(self) -> None:
        self.documents = [
            KnowledgeDocument("doc-a-1", "tenant-a", "供应商 A 最近出现交付延迟，需要关注履约风险。"),
            KnowledgeDocument("doc-a-2", "tenant-a", "供应商 A 合同要求关键事件在 24 小时内升级。"),
            KnowledgeDocument("doc-b-1", "tenant-b", "Tenant B 的私有经营资料，不得被其他租户检索。"),
        ]

    async def search(self, tenant_id: str, query: str, limit: int = 3) -> list[Evidence]:
        query_terms = {term for term in query.lower().split() if term}
        visible = [doc for doc in self.documents if doc.tenant_id == tenant_id]
        ranked = sorted(
            visible,
            key=lambda doc: sum(term in doc.content.lower() for term in query_terms),
            reverse=True,
        )
        return [
            Evidence(
                source_type="knowledge_base",
                source_id=doc.document_id,
                content=doc.content,
                confidence=0.85,
            )
            for doc in ranked[:limit]
        ]
