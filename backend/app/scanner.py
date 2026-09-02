from __future__ import annotations

import os
from pathlib import Path

from .config import IGNORED_DIRECTORIES, IGNORED_FILENAMES, MAX_INDEXABLE_FILE_BYTES, SUPPORTED_CODE_EXTENSIONS, SUPPORTED_DOCUMENT_EXTENSIONS, allowed_root
from .models import FileRecord, ScanSummary


class ScanError(ValueError):
    """Raised for a safe, user-facing repository scan failure."""


def scan_repository(raw_path: str) -> tuple[Path, list[FileRecord], ScanSummary]:
    root = Path(raw_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ScanError("Repository path was not found or is not a directory.")

    permitted_root = allowed_root()
    if permitted_root and not root.is_relative_to(permitted_root):
        raise ScanError("Repository path is outside the configured allowed root.")

    files: list[FileRecord] = []
    ignored_entries = 0
    for directory, directory_names, file_names in os.walk(root, topdown=True, followlinks=False):
        current = Path(directory)
        retained_directories: list[str] = []
        for name in directory_names:
            if name in IGNORED_DIRECTORIES or name == ".env":
                ignored_entries += 1
            else:
                retained_directories.append(name)
        directory_names[:] = retained_directories

        for filename in file_names:
            path = current / filename
            if filename in IGNORED_FILENAMES or filename.startswith(".env."):
                ignored_entries += 1
                continue
            record = _build_record(root, path)
            if record is None:
                ignored_entries += 1
                continue
            files.append(record)

    files.sort(key=lambda item: item.path.lower())
    code_files = sum(item.kind == "code" for item in files)
    documentation_files = len(files) - code_files
    return root, files, ScanSummary(files_detected=len(files), code_files=code_files, documentation_files=documentation_files, ignored_entries=ignored_entries)


def _build_record(root: Path, path: Path) -> FileRecord | None:
    try:
        if path.is_symlink() or not path.is_file():
            return None
        size = path.stat().st_size
        if size > MAX_INDEXABLE_FILE_BYTES or _is_binary(path):
            return None
    except OSError:
        return None

    extension = path.suffix.lower()
    if extension in SUPPORTED_CODE_EXTENSIONS:
        kind, language = "code", SUPPORTED_CODE_EXTENSIONS[extension]
    elif extension in SUPPORTED_DOCUMENT_EXTENSIONS:
        kind, language = "documentation", SUPPORTED_DOCUMENT_EXTENSIONS[extension]
    else:
        return None
    return FileRecord(path=path.relative_to(root).as_posix(), name=path.name, extension=extension, language=language, kind=kind, size_bytes=size)


def _is_binary(path: Path) -> bool:
    """Use a small byte sample to keep binary and media files out of the index."""
    try:
        with path.open("rb") as file:
            return b"\x00" in file.read(8_192)
    except OSError:
        return True
