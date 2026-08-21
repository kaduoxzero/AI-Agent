from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Protocol

from packages.contracts import Artifact


class ArtifactStore(Protocol):
    async def put(self, task_id: str, artifact: Artifact) -> str: ...
    async def get(self, uri: str) -> Artifact | None: ...
    async def close(self) -> None: ...


class InMemoryArtifactStore:
    def __init__(self) -> None:
        self._items: dict[str, Artifact] = {}
        self._lock = asyncio.Lock()

    async def put(self, task_id: str, artifact: Artifact) -> str:
        uri = f"memory://{task_id}/{artifact.artifact_id}"
        async with self._lock:
            self._items[uri] = artifact
        return uri

    async def get(self, uri: str) -> Artifact | None:
        async with self._lock:
            return self._items.get(uri)

    async def close(self) -> None:
        return None


class FileArtifactStore:
    """File-backed reference store with tenant-neutral opaque URIs.

    Object Storage implementations (S3/MinIO/GCS) should implement the same
    interface. Atomic replace avoids exposing partially written artifacts.
    """

    def __init__(self, root: str) -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, task_id: str, artifact_id: str) -> Path:
        safe_task = "".join(ch for ch in task_id if ch.isalnum() or ch in "-_")
        safe_artifact = "".join(ch for ch in artifact_id if ch.isalnum() or ch in "-_")
        path = (self.root / safe_task / f"{safe_artifact}.json").resolve()
        if self.root not in path.parents:
            raise ValueError("artifact path escaped root")
        return path

    async def put(self, task_id: str, artifact: Artifact) -> str:
        path = self._path(task_id, artifact.artifact_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        payload = artifact.model_dump_json(indent=2)

        def write() -> None:
            tmp.write_text(payload, encoding="utf-8")
            os.replace(tmp, path)

        await asyncio.to_thread(write)
        return f"file://{path.as_posix()}"

    async def get(self, uri: str) -> Artifact | None:
        if not uri.startswith("file://"):
            return None
        path = Path(uri.removeprefix("file://")).resolve()
        if self.root not in path.parents or not path.exists():
            return None
        raw = await asyncio.to_thread(path.read_text, encoding="utf-8")
        return Artifact.model_validate_json(raw)

    async def close(self) -> None:
        return None
