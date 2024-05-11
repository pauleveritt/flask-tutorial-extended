from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

api = Api(app, prefix="/v1")
ns = api.namespace("polls", description="Polls API")

from polls import views  # noqa: E402

# Create Tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    # Prevent the polls.view import from being cleaned up
    print(f"Importing views from {views}")
    app.run(debug=True)
