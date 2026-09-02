from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class RepositoryCreateRequest(BaseModel):
    local_path: str = Field(min_length=1, description="Absolute path to a local repository")


class FileRecord(BaseModel):
    path: str
    name: str
    extension: str
    language: str | None = None
    kind: Literal["code", "documentation"]
    size_bytes: int


class ScanSummary(BaseModel):
    files_detected: int
    code_files: int
    documentation_files: int
    ignored_entries: int


class Repository(BaseModel):
    id: str
    name: str
    local_path: str
    status: Literal["ready", "failed"]
    created_at: datetime
    summary: ScanSummary


class RepositoryCreated(BaseModel):
    repository: Repository
    files: list[FileRecord]
