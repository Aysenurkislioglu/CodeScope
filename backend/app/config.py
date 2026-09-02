from __future__ import annotations

import os
from pathlib import Path

SUPPORTED_CODE_EXTENSIONS = {
    ".py": "python", ".js": "javascript", ".jsx": "javascript",
    ".ts": "typescript", ".tsx": "typescript", ".java": "java",
    ".cpp": "cpp", ".c": "c", ".go": "go",
}
SUPPORTED_DOCUMENT_EXTENSIONS = {".md": "markdown", ".txt": "text", ".pdf": "pdf"}
IGNORED_DIRECTORIES = {".git", "node_modules", "venv", ".venv", "__pycache__", ".pytest_cache", "dist", "build", ".next", ".cache", "coverage", ".chroma"}
IGNORED_FILENAMES = {".env"}
MAX_INDEXABLE_FILE_BYTES = 1_000_000


def allowed_root() -> Path | None:
    """Return the optional root that local scans must remain inside."""
    value = os.getenv("REPOLENS_ALLOWED_ROOT")
    return Path(value).expanduser().resolve() if value else None
