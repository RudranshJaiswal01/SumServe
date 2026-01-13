from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_missing_input():
    response = client.post(
        "/api/summarize",
        data={"style": "brief"}
    )
    assert response.status_code == 400


def test_invalid_style():
    response = client.post(
        "/api/summarize",
        data={
            "style": "short",
            "text": "This is a valid input text for testing."
        }
    )
    assert response.status_code == 400


def test_text_too_short():
    response = client.post(
        "/api/summarize",
        data={
            "style": "brief",
            "text": "Too short"
        }
    )
    assert response.status_code == 400
