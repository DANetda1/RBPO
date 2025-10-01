from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get():
    payload = {
        "title": "Clean Architecture",
        "url": "https://example.com/ca",
        "tags": ["arch"],
        "priority": 2,
    }
    r = client.post("/reading-list", json=payload)
    assert r.status_code == 201
    created = r.json()
    assert created["id"] > 0
    assert created["status"] == "todo"
    r2 = client.get(f"/reading-list/{created['id']}")
    assert r2.status_code == 200
    assert r2.json()["title"] == "Clean Architecture"


def test_list_and_filters():
    client.post(
        "/reading-list",
        json={"title": "DDD Quickly", "tags": ["domain"], "priority": 3},
    )
    client.post(
        "/reading-list",
        json={"title": "CQRS Intro", "tags": ["arch", "domain"], "priority": 4},
    )
    r = client.get("/reading-list")
    assert r.status_code == 200
    assert len(r.json()) >= 2
    r2 = client.get("/reading-list", params={"tag": "domain"})
    assert all("domain" in i["tags"] for i in r2.json())
    r3 = client.get("/reading-list", params={"q": "intro"})
    assert all("intro" in i["title"].lower() for i in r3.json())


def test_update_status_and_delete():
    r = client.post("/reading-list", json={"title": "Refactoring"})
    item = r.json()
    r2 = client.patch(
        f"/reading-list/{item['id']}", json={"status": "done", "priority": 1}
    )
    assert r2.status_code == 200
    assert r2.json()["status"] == "done"
    assert r2.json()["priority"] == 1
    r3 = client.delete(f"/reading-list/{item['id']}")
    assert r3.status_code == 204
    r4 = client.get(f"/reading-list/{item['id']}")
    assert r4.status_code == 404


def test_validation():
    r = client.post("/reading-list", json={"title": ""})
    assert r.status_code == 422
