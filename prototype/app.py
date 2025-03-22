from sqlite3 import DatabaseError
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os, time

from models.player.player_manager import PlayerManager
from models.player.player import Player
from models.subject.subject import Subject
from models.subject.subject_manager import SubjectManager
from routes.study_routes import study_routes
from routes.authentication_routes import auth_routes
from routes.test_routes import test_routes
from models.database.db import db
from extensions import socketio
from flask_socketio import join_room, leave_room
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

app.secret_key = os.urandom(24)  # For session management
app.register_blueprint(study_routes, url_prefix="/api")
app.register_blueprint(test_routes, url_prefix="/test")
app.register_blueprint(auth_routes)

socketio.init_app(app)

@socketio.on("join")
def handle_join(data):
    """Join a user-specific room"""
    print(f"Someone is trying to join a room:", data)
    room = data.get("room")
    user_id = data.get("user_id")
    if room:
        join_room(room)  # ✅ Join the room
        print(f"User {user_id} joined room {room}")

@socketio.on("leave")
def handle_leave(data):
    """Leave a user-specific room"""
    user_id = data.get("user_id")
    if user_id:
        leave_room(f"user_{user_id}")  # ✅ Leave the room
        print(f"User {user_id} left room user_{user_id}")

@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
        
    player: Player = PlayerManager.get(session['user_id'])
    if not player:
        return redirect(url_for('auth.login'))
        
    subjects = []

    for subject in SubjectManager.get_all(session['user_id']):
        subjects.append(Subject(
            id=subject["subject_id"],
            code_name=subject["code_name"],
            difficulty=subject["difficulty"],
            user_id=subject["user_id"]
        ))

    return render_template("index.html",
        player=player,
        subjects=subjects
    )

@app.errorhandler(400)
def handle_bad_request(e):
    return jsonify({"error": "Bad Request", "message": e.description}), 400

if __name__ == "__main__":
    app.run(debug=True)
