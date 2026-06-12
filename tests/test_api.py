from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_ask_returns_answer():
    with patch("app.main.answer_with_sources", return_value=("Capital must be 8% of RWA [1].", [])):
        resp = client.post("/ask", json={"question": "What is the capital requirement?", "k": 3})
    assert resp.status_code == 200
    assert resp.json()["answer"] == "Capital must be 8% of RWA [1]."
    assert resp.json()["sources"] == []


def test_ask_uses_default_k():
    with patch("app.main.answer_with_sources", return_value=("Some answer.", [])) as mock_fn:
        client.post("/ask", json={"question": "What is OSFI?"})
        mock_fn.assert_called_once_with("What is OSFI?", 8)


def test_ask_empty_question_returns_validation_error():
    resp = client.post("/ask", json={"question": ""})
    assert resp.status_code == 422


def test_ask_question_too_long_returns_validation_error():
    resp = client.post("/ask", json={"question": "x" * 2001})
    assert resp.status_code == 422


def test_ask_returns_sources():
    sources = [{"source": "osfi.pdf", "page": 3}, {"source": "basel.pdf", "page": 7}]
    with patch("app.main.answer_with_sources", return_value=("Answer with sources [1].", sources)):
        resp = client.post("/ask", json={"question": "What are capital requirements?", "k": 2})
    assert resp.status_code == 200
    data = resp.json()
    assert data["sources"] == sources
