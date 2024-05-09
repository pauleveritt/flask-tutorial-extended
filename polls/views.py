from . import serializers
from .models import Question, Choice
from flask import request
from flask_restx import Resource
from . import serializers
from .main import db, ns
import json


@ns.route('/questions')
class QuestionList(Resource):
    @ns.marshal_with(serializers.question_serializer, envelope='questions')
    def get(self):
        return Question.query.all()

    @ns.expect(serializers.question_choice_serializer)
    @ns.marshal_with(serializers.question_choice_serializer, code=201)
    def post(self):
        data = json.loads(request.data.decode())
        question_text = data['question_text']
        choices = data['choices']

        # Create the question
        question = Question(question_text=question_text)
        db.session.add(question)
        db.session.commit()

        # Create choices for the question
        for choice_text in choices:
            choice = Choice(question_id=question.id, choice_text=choice_text)
            db.session.add(choice)
        db.session.commit()

        return {'question_text': question_text, 'choices': choices}, 201


@ns.route('/questions/<int:question_id>')
class QuestionDetail(Resource):
    @ns.marshal_with(serializers.question_serializer)
    def get(self, question_id):
        return Question.query.get_or_404(question_id)

    @ns.expect(serializers.question_choice_serializer)
    @ns.marshal_with(serializers.question_choice_serializer)
    def put(self, question_id):
        data = json.loads(request.data.decode())
        question_text = data['question_text']
        choices = data['choices']

        # Update the question text
        question = Question.query.get_or_404(question_id)
        question.question_text = question_text

        # Delete existing choices and create new choices for the question
        Choice.query.filter_by(question_id=question_id).delete()
        for choice_text in choices:
            choice = Choice(question_id=question.id, choice_text=choice_text)
            db.session.add(choice)

        db.session.commit()

        return {'question_text': question_text, 'choices': choices}

    @ns.response(204, 'Question deleted')
    def delete(self, question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return '', 204
