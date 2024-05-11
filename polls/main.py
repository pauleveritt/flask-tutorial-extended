import os
import click
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from flask.cli import with_appcontext

APP_ENV = os.getenv("APP_ENV", default="development")

if APP_ENV == "development":
    DB_NAME = "sqlite:///database.db"
elif APP_ENV == "testing":
    DB_NAME = "sqlite:///test.db"
else:
    raise NotImplementedError("DB NAME Missing!")

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
db = SQLAlchemy(app)

api = Api(app)
ns = api.namespace('polls', description='Polls API')

from polls import views  # noqa: E402

# Create Tables
with app.app_context():
    db.create_all()


@click.command(name='seed')
@with_appcontext
def seed():
    from .seed import create_seed_data
    create_seed_data()


# Register Commands
app.cli.add_command(seed)
if __name__ == '__main__':
    # Prevent the polls.view import from being cleaned up
    print(f'Importing views from {views}')
    app.run(debug=True)
