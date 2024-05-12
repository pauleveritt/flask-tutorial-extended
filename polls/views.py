import json

from flask import request, render_template
from flask_restx import Resource

from polls import serializers
from polls.main import db, ns, app
from polls.models import Question, Choice


@ns.route("/questions")
class QuestionList(Resource):
    @ns.marshal_with(serializers.question_serializer)
    def get(self):
        return Question.query.all()

    @ns.expect(serializers.question_choice_serializer)
    @ns.marshal_with(serializers.question_choice_serializer, code=201)
    def post(self):
        data = json.loads(request.data.decode())
        question_text = data["question_text"]
        choices = data["choices"]

        # Create the question
        question = Question(question_text=question_text)
        db.session.add(question)
        db.session.commit()

        # Create choices for the question
        for choice_text in choices:
            choice = Choice(question_id=question.id, choice_text=choice_text)
            db.session.add(choice)
        db.session.commit()

        return {"question_text": question_text, "choices": choices}, 201


@ns.route("/questions/<int:question_id>")
class QuestionDetail(Resource):
    @ns.marshal_with(serializers.question_serializer)
    def get(self, question_id):
        return Question.query.get_or_404(question_id)

    @ns.expect(serializers.question_choice_serializer)
    @ns.marshal_with(serializers.question_choice_serializer)
    def put(self, question_id):
        data = json.loads(request.data.decode())
        question_text = data["question_text"]
        choices = data["choices"]

        # Update the question text
        question = Question.query.get_or_404(question_id)
        question.question_text = question_text

        # Delete existing choices and create new choices for the question
        Choice.query.filter_by(question_id=question_id).delete()
        for choice_text in choices:
            choice = Choice(question_id=question.id, choice_text=choice_text)
            db.session.add(choice)

        db.session.commit()

        return {"question_text": question_text, "choices": choices}

    @ns.response(204, "Question deleted")
    def delete(self, question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return "", 204


# Some HTML routes
@app.route("/polls/")
def index_html():
    questions = Question.query.all()
    return render_template("index.html", questions=questions)


@app.route("/polls/questions/")
def questions_html():
    questions = Question.query.all()
    return render_template("questions.html", questions=questions)


@app.route("/polls/questions/<int:question_id>")
def question_html(question_id: int):
    question = Question.query.get_or_404(question_id)
    return render_template("question.html", question=question)
