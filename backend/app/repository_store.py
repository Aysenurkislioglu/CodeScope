from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from .models import FileRecord, Repository
from .scanner import scan_repository


class RepositoryStore:
    """Small in-memory store for the scanner MVP."""

    def __init__(self) -> None:
        self._repositories: dict[str, Repository] = {}
        self._files: dict[str, list[FileRecord]] = {}

    def create_and_scan(self, local_path: str) -> tuple[Repository, list[FileRecord]]:
        root, files, summary = scan_repository(local_path)
        repository = Repository(id=str(uuid4()), name=root.name, local_path=str(root), status="ready", created_at=datetime.now(UTC), summary=summary)
        self._repositories[repository.id] = repository
        self._files[repository.id] = files
        return repository, files

    def list(self) -> list[Repository]:
        return sorted(self._repositories.values(), key=lambda item: item.created_at, reverse=True)

    def get(self, repository_id: str) -> Repository | None:
        return self._repositories.get(repository_id)

    def files_for(self, repository_id: str) -> list[FileRecord] | None:
        return self._files.get(repository_id)
