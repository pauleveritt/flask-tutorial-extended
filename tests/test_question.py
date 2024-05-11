import pytest
from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from polls.main import app, db
from polls.seed import questions_data


@pytest.fixture
def client() -> FlaskClient:
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.rollback()  # Rollback any changes to the database
            db.drop_all()


def test_post_question(client):
    # Send POST request to create a new question with choices
    data = {
        "question_text": "What is your favorite programming language?",
        "choices": ["Python", "Java", "JavaScript"],
    }
    response = client.post("/polls/questions", json=data)
    assert response.status_code == 201


def test_read_questions_html(client):
    # Use the existing seed data
    response = client.get("/polls/")
    assert response.status_code == 200
    html = BeautifulSoup(response.text, "html5lib")
    questions = html.select(".question_text a")
    assert len(questions) == len(questions_data)
    assert questions[0].attrs["href"] == "http://testserver/question/1"
    assert questions[0].text == questions_data[0]["question_text"]
