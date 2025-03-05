from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from models import Player, Subject
from routes.study_routes import study_routes

app = Flask(__name__)
app.register_blueprint(study_routes, url_prefix="/api")

player = Player(1, "player@example.com", "Sung Jin-Woo", "password", level=777777, exp=7777777)

subjects = [
    Subject("SoftEng", "Software Engineering", 3),
    Subject("Science", "Science 401", 2),
    Subject("History", "History", 4),
    Subject("Math", "Mathematics", 3)
]

@app.route("/")
def index():
    return render_template("index.html",
        player=player.to_dict(),
        subjects=[s.to_dict() for s in subjects]
    )

if __name__ == "__main__":
    app.run(debug=True)
