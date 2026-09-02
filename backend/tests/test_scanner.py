from pathlib import Path

import pytest

from app.scanner import ScanError, scan_repository


def test_scans_supported_files_and_ignores_secrets_and_dependencies(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "src" / "main.py").write_text("def greet():\n    return 'hi'\n")
    (tmp_path / "README.md").write_text("# Demo\n")
    (tmp_path / ".env").write_text("API_KEY=never-index-this")
    (tmp_path / "node_modules" / "package.js").write_text("export default {}")
    (tmp_path / "image.png").write_bytes(b"\x89PNG\x00binary")

    _, files, summary = scan_repository(str(tmp_path))
    assert [file.path for file in files] == ["README.md", "src/main.py"]
    assert summary.files_detected == 2
    assert summary.code_files == 1
    assert summary.documentation_files == 1
    assert summary.ignored_entries == 3


def test_requires_an_existing_directory(tmp_path: Path) -> None:
    with pytest.raises(ScanError, match="not found"):
        scan_repository(str(tmp_path / "missing"))
