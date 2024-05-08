import pytest


@pytest.fixture
def client():
    from polls.main import app, db, DB_NAME
    from polls.models import Question, Choice

    DB_NAME = 'sqlite:///test.db'  # Use a separate test database
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.rollback()  # Rollback any changes to the database
            # db.drop_all()


def test_create_question(client):
    # Create a new question
    response = client.post('/polls/questions', json={'question_text': 'What is your favorite color?'})
    assert response.status_code == 201
    assert response.json['question_text'] == 'What is your favorite color?'
