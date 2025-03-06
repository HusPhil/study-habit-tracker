from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from datetime import datetime
from models.player import Player
from models.subject import Subject
from routes.study_routes import study_routes
from routes.authentication_routes import auth_routes
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
app.register_blueprint(study_routes, url_prefix="/api")
app.register_blueprint(auth_routes)

@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    player = Player.get(session['user_id'])
    if not player:
        return redirect(url_for('auth.login'))
        
    subjects = []
    return render_template("index.html",
        player=player,
        subjects=subjects
    )
    
if __name__ == "__main__":
    app.run(debug=True)
