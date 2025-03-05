from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from models import Player, Subject, Quest
from routes.study_routes import study_routes

app = Flask(__name__)
app.register_blueprint(study_routes, url_prefix="/api")

# First check if player exists
player = Player.get(1)  # Try to get existing player

if not player:  # Only create if doesn't exist
    player = Player.create(
        email="test@example.com",
        username="test_user",
        password="test_password"
    )
subjects = [
    Subject("SoftEng", "SoftEng", 3),
    Subject("Science", "Science 401", 2),
    Subject("History", "History", 4),
    Subject("Math", "Mathematics", 3),
    Subject("Math", "Mathematics", 3),
    Subject("Math", "Mathematics", 5),
    Subject("Math", "Mathematics", 3),
    Subject("Super", "Super Hard Subject", 5),
]

subjects[0].add_quest(quest = Quest("Complete Chapter 1", difficulty="medium"))

@app.route("/")
def index():
    return render_template("index.html",
        player=player,
        subjects=subjects
    )

if __name__ == "__main__":
    app.run(debug=True)
