import click
from flask import Flask
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

api = Api(app, prefix="/v1")
ns = api.namespace("polls", description="Polls API")

from polls import views  # noqa: E402

# Create Tables
with app.app_context():
    db.create_all()


@click.command(name="seed")
@with_appcontext
def seed():
    from polls.seed import create_seed_data

    create_seed_data()


# Register Commands
app.cli.add_command(seed)
if __name__ == "__main__":
    # Prevent the polls.view import from being cleaned up
    print(f"Importing views from {views}")
    app.run(debug=True)
