from sqlite3 import DatabaseError
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
from datetime import datetime

from models.player import Player
from models.subject import Subject
from routes.study_routes import study_routes
from routes.authentication_routes import auth_routes
import os
from models.db import db

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
        
    subjects = Subject.get_all(session['user_id'])
    
    return render_template("index.html",
        player=player,
        subjects=subjects
    )

@app.route('/route_tester', methods=['POST'])
def route_tester():
    print(request.form)
    return jsonify({
        'message': 'Route tester endpoint'
    })
    
if __name__ == "__main__":
    app.run(debug=True)
