from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
from models import Player
from routes.study_routes import study_routes

app = Flask(__name__)
app.register_blueprint(study_routes, url_prefix="/api")

DATA_FILE = "study_data.json"

@app.route("/")
def index():
    player1 = Player(1, "player@example.com", "GamerJohn", "securePass123")

    player1.login()
    print(player1.level)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
