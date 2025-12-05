from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crud_links():
    # Create
    resp = client.post("/api/links", json={"original_url": "https://example.com/long", "short_name": "exmpl"})
    assert resp.status_code == 201
    link_id = resp.json()["id"]

    # Read
    resp = client.get(f"/api/links/{link_id}")
    assert resp.status_code == 200

    # List
    resp = client.get("/api/links")
    assert resp.status_code == 200
    assert any(l["id"] == link_id for l in resp.json())

    # Update
    resp = client.put(f"/api/links/{link_id}", json={"original_url": "https://example.com/long2", "short_name": "exmpl2"})
    assert resp.status_code == 200
    assert resp.json()["short_name"] == "exmpl2"

    # Delete
    resp = client.delete(f"/api/links/{link_id}")
    assert resp.status_code == 204

    # Not found
    resp = client.get(f"/api/links/{link_id}")
    assert resp.status_code == 404
