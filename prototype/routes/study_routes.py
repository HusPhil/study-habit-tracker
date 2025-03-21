from flask import Blueprint, request, jsonify, redirect, url_for, session
from typing import Dict
from models import Subject, Quest, Session  # Import the Subject model
from models.enemy.enemy import Enemy
from models.player.player_manager import PlayerManager
from models.player.player import Player
from models.session.session import SessionManager
from extensions import socketio
import time

study_routes = Blueprint("study_routes", __name__)  # Define Blueprint

# Start Session Route
@study_routes.route("/start_session", methods=["POST"])
def start_session():
    try:
        data = request.json
        subject = Subject.get(data["subject_id"])
        selected_quests: list = data["selected_quests"]
        battle_duration = int(data["battle_duration"])
        user_id = data["user_id"]

        print("selectedQuests", selected_quests)

        enemies: list[Enemy] = subject.spawnEnemy(selected_quests)  
        
        session = Session(
            id=int(time.time()), 
            subject_id=subject.id, 
            duration=battle_duration, 
            goals=selected_quests
        )
        
        if session.id in SessionManager.active_sessions:
            return jsonify("Session already started")

        session_data = session.start(user_id=int(user_id), socketio=socketio)

        print("enemies", enemies, session_data)

        # if session_data.get("error"):
        #     return jsonify({"error": f"Invalid request: {str(e)}"})   

        return jsonify({
            "session_data": session_data, 
            "enemies": [enemy.to_dict() for enemy in enemies],
        })
    
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@study_routes.route("/stop_session", methods=["POST"])
def stop_session():
    user_id = session.get("user_id")  # Ensure we get an integer user_id
    if user_id is None:
        return jsonify({"error": "User ID not found in session"}), 400

    current_session: Session = SessionManager.active_sessions.get(user_id)
    if not current_session:
        return jsonify({"error": "No active session found for this user"}), 404

    session_data = current_session.stop(user_id=user_id, socketio=socketio)

    data = request.get_json()

    remaining_enemies = data["remaining_enemies"]

    player = Player(**PlayerManager.get(user_id))
    player.gain_exp(PlayerManager.calculate_exp(total_enemies=data["total_enemies"], remaining_enemies=remaining_enemies)["net_exp"])
    PlayerManager.save(player.to_dict())
    return jsonify({"message": "Session stopped successfully"})

@study_routes.route("/subject/get_by_id", methods=["GET"])
def get_subject():
    try:
        subject_id = request.args.get('subject_id', type=int)
        if not subject_id:
            return jsonify({"error": "subject_id parameter is required"}), 400
            
        subject = Subject.get(subject_id)
        if not subject:
            return jsonify({"error": "Subject not found"}), 404
            
        return jsonify({
            "subject": subject.to_dict()
        })
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@study_routes.route("/subject/create", methods=["POST"])
def create_subject():
    try:
        Subject.create(
            user_id=request.form["user_id"],
            code_name=request.form["code_name"],
            description=request.form["description"],
            difficulty=request.form["subjectDifficulty"]
        )
        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@study_routes.route("/subject/get_quests", methods=["GET"])
def get_subject_quests():
    subject_id = request.args.get("subject_id")  # ✅ Get subject ID from query params

    if not subject_id:
        return jsonify({"error": "Subject ID is required"}), 400

    try:    
        subject = Subject.get(subject_id)  # ✅ Fetch subject by ID
        quests = [quest.to_dict() for quest in subject.get_quests()]  # ✅ Convert quests to JSON
        return jsonify(quests)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@study_routes.route("/subject/get_flashcards", methods=["GET"])
def get_subject_flashcards():
    subject_id = request.args.get("subject_id")  # ✅ Get subject ID from query params

    if not subject_id:
        return jsonify({"error": "Subject ID is required"}), 400

    try:
        # Convert subject_id to int (assuming IDs are integers)
        subject_id = int(subject_id)

        # Fetch subject by ID
        subject = Subject.get(subject_id)

        if not subject:
            return jsonify({"error": f"Subject with ID {subject_id} not found"}), 404

        # Fetch and convert flashcards
        flashcards = subject.get_flashcards() or []  # Ensure it's a list
        flashcards_data = [flashcard.to_dict() for flashcard in flashcards]

        print(f"MY FLASHCARDS AT SUBJECT {subject.code_name}", flashcards_data)
        return jsonify(flashcards_data)

    except ValueError:
        return jsonify({"error": "Invalid Subject ID format"}), 400  # Handles non-integer subject_id

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@study_routes.route("/subject/get_notes", methods=["GET"])
def get_subject_notes():
    subject_id = request.args.get("subject_id")  # ✅ Get subject ID from query params

    if not subject_id:
        return jsonify({"error": "Subject ID is required"}), 400

    try:
        # Convert subject_id to int (assuming IDs are integers)
        subject_id = int(subject_id)

        # Fetch subject by ID
        subject = Subject.get(subject_id)

        if not subject:
            return jsonify({"error": f"Subject with ID {subject_id} not found"}), 404

        # Fetch and convert flashcards
        notes = subject.get_notes() or []  # Ensure it's a list
        notes_data = [note.to_dict() for note in notes]

        print(f"MY NOTES AT SUBJECT {subject.code_name}", notes_data)
        return jsonify(notes_data)

    except ValueError:
        return jsonify({"error": "Invalid Subject ID format"}), 400  # Handles non-integer subject_id

    except Exception as e:
        return jsonify({"error": str(e)}), 500




@study_routes.route("/subject/get_all_by_user_id", methods=["GET"])
def get_all_by_user_id():
    try:
        print(request.args)
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"error": "user_id parameter is required"}), 400
            
        subjects = Subject.get_all(user_id)
        return jsonify([subject.to_dict() for subject in subjects])
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@study_routes.route("/quest/create", methods=["POST"])
def create_quest():
    try:
        print(request.form)
        newQuest = Quest.create(
            description=request.form["description"],
            difficulty=request.form["questDifficulty"],
            subject_id=request.form["subject_id"]
        )
        return newQuest.to_dict()
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@study_routes.route("/quest/get_by_subject_id", methods=["GET"])
def get_quest_by_subject_id():
    try:
        subject_id = request.args.get('subject_id', type=int)
        if not subject_id:
            return jsonify({"error": "subject_id parameter is required"}), 400
            
        quests = Quest.get_by_subject_id(subject_id)
        return jsonify({"quests": [quest.to_dict() for quest in quests]})
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@study_routes.route("/quest/update_status/<int:quest_id>", methods=["POST"])
def update_quest_status(quest_id):
    try:
        data: Dict = request.get_json()
        
        if "status" not in data:
            return jsonify({"error": "status field is required"}), 400
            
        status = data["status"]
        if not isinstance(status, int) or status not in [0, 1, 2]:
            return jsonify({"error": "status must be 0, 1, or 2"}), 400
            
        quest = Quest.get(quest_id)
        if not quest:
            return jsonify({"error": "Quest not found"}), 404
            
        quest.status = status
        quest.save()
        
        return jsonify({
            "message": "Quest status updated successfully",
            "quest": quest.to_dict()
        })
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
