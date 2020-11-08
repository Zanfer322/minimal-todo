from fastapi.testclient import TestClient


def test_create_tag(client: TestClient) -> None:
    res = client.post("/api/tags/", json={"name": "tag name"})
    assert res.status_code == 200
    assert res.json()["name"] == "tag name"


def test_create_multiple_tags(client: TestClient) -> None:
    res = client.post("/api/tags/", json={"name": "tag 1"})
    assert res.status_code == 200
    res = client.post("/api/tags/", json={"name": "tag 2"})
    assert res.status_code == 200

    res = client.get("/api/tags/")
    assert res.status_code == 200
    data = res.json()

    assert len(data) == 2
    assert set([x["name"] for x in data]) == {"tag 1", "tag 2"}


def test_get_id(client: TestClient) -> None:
    res = client.post("/api/tags/", json={"name": "tag name"})
    assert res.status_code == 200

    id = res.json()["id"]
    res = client.get(f"/api/tags/{id}")
    assert res.status_code == 200
    assert res.json()["name"] == "tag name"


def test_get_unknown_id(client: TestClient) -> None:
    res = client.post("/api/tags/", json={"name": "tag name"})
    assert res.status_code == 200

    res = client.get("/api/tags/hi")
    assert res.status_code == 404


def test_get_name(client: TestClient) -> None:
    res = client.post("/api/tags/", json={"name": "tag name"})
    assert res.status_code == 200

    id = res.json()["id"]
    res = client.get("/api/tags/name", params={"name": "tag name"})
    assert res.status_code == 200
    assert res.json()["id"] == id


def test_get_unknown_name(client: TestClient) -> None:
    res = client.post("/api/tags/", json={"name": "tag name"})
    assert res.status_code == 200

    res = client.get("/api/tags/name", params={"name": "unknown name"})
    assert res.status_code == 404
