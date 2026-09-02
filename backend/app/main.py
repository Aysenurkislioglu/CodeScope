from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .models import Repository, RepositoryCreateRequest, RepositoryCreated
from .repository_store import RepositoryStore
from .scanner import ScanError

app = FastAPI(title="RepoLens API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
store = RepositoryStore()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/repositories", response_model=RepositoryCreated, status_code=status.HTTP_201_CREATED)
def add_repository(payload: RepositoryCreateRequest) -> RepositoryCreated:
    try:
        repository, files = store.create_and_scan(payload.local_path)
        return RepositoryCreated(repository=repository, files=files)
    except ScanError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/api/repositories", response_model=list[Repository])
def list_repositories() -> list[Repository]:
    return store.list()


@app.get("/api/repositories/{repository_id}", response_model=Repository)
def get_repository(repository_id: str) -> Repository:
    repository = store.get(repository_id)
    if repository is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found.")
    return repository


@app.get("/api/repositories/{repository_id}/files")
def list_files(repository_id: str):
    files = store.files_for(repository_id)
    if files is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found.")
    return files
