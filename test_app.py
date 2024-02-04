from fastapi.testclient import TestClient
from .app import app


client = TestClient(app)


def test_create_form():
    response = client.post(
        "/new-form/",
        json={
            "name": "create-vue",
            "questions": [
                {
                    "name": "project-name",
                    "description": None,
                    "allows_multiple_answer": False,
                    "variants": [],
                },
                {
                    "name": "version",
                    "description": None,
                    "allows_multiple_answer": False,
                    "variants": ["1", "2", "3"],
                },
                {
                    "name": "include",
                    "description": None,
                    "allows_multiple_answer": True,
                    "variants": ["Pinia", "Vitest", "TypeScript", "VueRouter"],
                },
            ],
        },
    )
    print(response.json())
    assert response.status_code == 200
