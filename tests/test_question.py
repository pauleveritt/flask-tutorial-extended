import os

import pytest

from polls.main import app, db


@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.rollback()  # Rollback any changes to the database
            db.drop_all()
            os.remove("instance/test.db")


def test_post_question(client):
    # Send POST request to create a new question with choices
    data = {
        "question_text": "What is your favorite programming language?",
        "choices": ["Python", "Java", "JavaScript"],
    }
    response = client.post("/polls/questions", json=data)
    assert response.status_code == 201
