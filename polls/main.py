import os

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

APP_ENV = os.getenv("APP_ENV")

if APP_ENV == "development":
    DB_NAME = "sqlite:///database.db"
elif APP_ENV == "testing":
    DB_NAME = "sqlite:///test.db"
else:
    raise NotImplemented("DB NAME Missing!")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
db = SQLAlchemy(app)

api = Api(app)
ns = api.namespace('polls', description='Polls API')

from . import views

# Create Tables
with app.app_context():
    from . import models
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
