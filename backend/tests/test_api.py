from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app, store


def test_health_endpoint() -> None:
    client = TestClient(app)
    assert client.get("/api/health").json() == {"status": "ok"}


def test_add_and_list_repository(tmp_path: Path) -> None:
    store._repositories.clear()
    store._files.clear()
    (tmp_path / "app.py").write_text("print('ok')\n")
    client = TestClient(app)
    created = client.post("/api/repositories", json={"local_path": str(tmp_path)})
    assert created.status_code == 201
    body = created.json()
    assert body["repository"]["summary"]["files_detected"] == 1
    assert body["files"][0]["path"] == "app.py"
    assert len(client.get("/api/repositories").json()) == 1
