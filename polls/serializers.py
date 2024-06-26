from flask_restx import fields

from polls.main import api

question_serializer = api.model(
    "Question",
    {
        "id": fields.Integer,
        "question_text": fields.String(required=True, description="Question text"),
    },
)

choice_serializer = api.model(
    "Choice",
    {
        "choice_text": fields.String(required=True, description="Choice text"),
        "votes": fields.Integer(required=True, description="Number of votes"),
    },
)

question_choice_serializer = api.model(
    "QuestionChoice",
    {
        "question_text": fields.String(required=True, description="Question text"),
        "choices": fields.List(fields.String(required=True, description="Choice text")),
    },
)
