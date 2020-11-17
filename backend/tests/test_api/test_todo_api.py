from typing import Set

from fastapi.testclient import TestClient


def _create_tags(client: TestClient, tags: Set[str]) -> None:
    for tag in tags:
        res = client.post("/api/tags/", json={"name": tag})
        assert res.status_code == 200


def test_create_todo(client: TestClient) -> None:
    _create_tags(client, {"tag1", "tag2"})

    res = client.post(
        "/api/todo/", json={"contents": "content", "tags": ["tag1", "tag2"]}
    )
    assert res.status_code == 200
    assert res.json()["contents"] == "content"


def test_create_multiple_todos(client: TestClient) -> None:
    _create_tags(client, {"tag1", "tag2"})

    res = client.post("/api/todo/", json={"contents": "content 1", "tags": ["tag1"]})
    assert res.status_code == 200

    res = client.post("/api/todo/", json={"contents": "content 2", "tags": ["tag2"]})
    assert res.status_code == 200

    res = client.get("/api/todo")
    assert res.status_code == 200
    data = res.json()

    assert len(data) == 2
    assert set([x["contents"] for x in data]) == {"content 1", "content 2"}


def test_get_id(client: TestClient) -> None:
    res = client.post("/api/todo/", json={"contents": "content 1", "tags": []})
    assert res.status_code == 200

    id = res.json()["id"]
    res = client.get(f"/api/todo/{id}")
    assert res.status_code == 200
    assert res.json()["contents"] == "content 1"


def test_get_unknown_id(client: TestClient) -> None:
    res = client.post("/api/todo/", json={"contents": "content 1", "tags": []})
    assert res.status_code == 200

    res = client.get("/api/todo/hi")
    assert res.status_code == 404


def test_update_todo(client: TestClient) -> None:
    _create_tags(client, {"tag1"})

    res = client.post("/api/todo/", json={"contents": "content 1", "tags": []})
    assert res.status_code == 200

    res = client.put(
        "/api/todo/",
        json={
            "id": res.json()["id"],
            "contents": "new content",
            "tags": ["tag1"],
            "state": "done",
        },
    )
    assert res.status_code == 200, res.text
    assert res.json()["contents"] == "new content"


def test_search_todos(client: TestClient) -> None:
    _create_tags(client, {"tag1", "tag2"})

    res = client.post(
        "/api/todo/", json={"contents": "some contents", "tags": ["tag1"]}
    )
    assert res.status_code == 200

    res = client.post(
        "/api/todo/", json={"contents": "other contents", "tags": ["tag2"]}
    )
    assert res.status_code == 200
    id = res.json()["id"]

    res = client.get("/api/todo/search", params={"search_term": "other"})
    assert res.status_code == 200

    data = res.json()
    assert len(data) == 1
    assert data[0]["id"] == id
