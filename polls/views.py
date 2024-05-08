from . import serializers
from .models import Question
from flask import request
from flask_restx import Resource
from . import serializers
from .main import db, ns


@ns.route('/questions')
class QuestionList(Resource):
    @ns.marshal_with(serializers.question_serializer, envelope='questions')
    def get(self):
        return Question.query.all()

    @ns.expect(serializers.question_serializer)
    @ns.marshal_with(serializers.question_serializer, code=201)
    def post(self):
        data = request.json
        new_question = Question(question_text=data['question_text'])
        db.session.add(new_question)
        db.session.commit()
        return new_question, 201


@ns.route('/questions/<int:question_id>')
class QuestionDetail(Resource):
    @ns.marshal_with(serializers.question_serializer)
    def get(self, question_id):
        return Question.query.get_or_404(question_id)

    @ns.expect(serializers.question_serializer)
    @ns.marshal_with(serializers.question_serializer)
    def put(self, question_id):
        question = Question.query.get_or_404(question_id)
        data = request.json
        question.question_text = data['question_text']
        db.session.commit()
        return question

    @ns.response(204, 'Question deleted')
    def delete(self, question_id):
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return '', 204
