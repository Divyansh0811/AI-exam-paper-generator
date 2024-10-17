import pytest
from fastapi.testclient import TestClient
from app.main import app 

client = TestClient(app)


def test_create_paper():
    paper_data = {
        "title": "Sample Paper",
        "type": "exam",
        "time": 60,
        "marks": 100,
        "params": {
            "board": "CBSE",
            "grade": 10,
            "subject": "Mathematics"
        },
        "tags": ["math", "exam"],
        "chapters": ["Algebra", "Geometry"],
        "sections": [
            {
                "marks_per_question": 5,
                "type": "MCQ",
                "questions": [
                    {
                        "question": "What is 2 + 2?",
                        "answer": "4",
                        "type": "multiple_choice",
                        "question_slug": "simple_addition",
                        "reference_id": "Q001",
                        "hint": "Use basic addition.",
                        "params": {}
                    }
                ]
            }
        ]
    }

    response = client.post("/paper", json=paper_data)
    assert response.status_code == 200
    assert "id" in response.json()
