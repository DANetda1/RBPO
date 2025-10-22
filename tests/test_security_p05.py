from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app
from app.settings import Settings

client = TestClient(app)


def test_problem_json_with_correlation_id():
    r = client.get("/items/999999")
    assert r.status_code == 404
    assert r.headers.get("content-type", "").startswith("application/problem+json")
    body = r.json()
    assert body["status"] == 404
    UUID(str(body["correlation_id"]))


def test_settings_load_from_env(monkeypatch):
    monkeypatch.setenv(
        "ALLOWED_ORIGINS", '["http://localhost:3000","http://example.com"]'
    )
    s = Settings()
    assert "http://example.com" in s.ALLOWED_ORIGINS


def test_large_payload_returns_413():
    big = "x" * (1 * 1024 * 1024 + 10)
    r = client.post("/health", data=big, headers={"content-type": "text/plain"})
    assert r.status_code == 413
    assert r.headers.get("content-type", "").startswith("application/problem+json")
    body = r.json()
    assert body["status"] == 413
    UUID(str(body["correlation_id"]))


def test_create_item_validation_error_problem_json():
    r = client.post("/items", params={"name": ""})
    assert r.status_code == 422
    assert r.headers.get("content-type", "").startswith("application/problem+json")
    body = r.json()
    assert body["status"] == 422
    UUID(str(body["correlation_id"]))
