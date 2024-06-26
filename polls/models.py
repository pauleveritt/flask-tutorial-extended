from datetime import datetime, timedelta

from polls.main import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(200))
    pub_date = db.Column(db.DateTime, default=datetime.now())
    choices = db.relationship('Choice', backref='question', lazy='dynamic')

    def was_published_recently(self):
        now = datetime.now()
        return now - timedelta(days=1) <= self.pub_date <= now

    def __repr__(self):
        return self.question_text


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    choice_text = db.Column(db.String(200))
    votes = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.choice_text
