from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def seed_links():
    for i in range(1, 21):
        client.post("/api/links", json={"original_url": f"https://example.com/{i}", "short_name": f"link{i}"})

def test_pagination_first_10():
    resp = client.get("/api/links?range=[0,10]")
    assert resp.status_code == 200
    assert resp.headers["Content-Range"].startswith("links 0-10/")
    assert len(resp.json()) == 10

def test_pagination_skip_5_next_5():
    resp = client.get("/api/links?range=[5,10]")
    assert resp.status_code == 200
    assert resp.headers["Content-Range"].startswith("links 5-10/")
    assert len(resp.json()) == 5
