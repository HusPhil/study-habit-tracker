from flask import Blueprint, request, jsonify, redirect, url_for, session
from typing import Dict
from models import Subject, Quest, Session  # Import the Subject model
from models.enemy.enemy import Enemy

from models.player.player import Player
from models.player.player_manager import PlayerManager

from models.session.session import SessionManager

from models.subject.subject_manager import SubjectManager
from models.quest.quest_manager import QuestManager

from extensions import socketio
import time

study_routes = Blueprint("study_routes", __name__)  # Define Blueprint

# Start Session Route
@study_routes.route("/start_session", methods=["POST"])
def start_session():
    try:
        data = request.json
        subject = SubjectManager.get(data["subject_id"])
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
            
        subject = SubjectManager.get(subject_id)
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
        SubjectManager.create(
            user_id=request.form["user_id"],
            code_name=request.form["code_name"],
            description=request.form["description"],
            difficulty=request.form["subjectDifficulty"]
        )
        return redirect(url_for('index'))

    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
    
@study_routes.route("/subject/get_all_by_user_id", methods=["GET"])
def get_all_by_user_id():
    try:
        print("GETTING ALL THE SUBJECTS")

        # Validate user_id parameter
        user_id = int(request.args.get('user_id'))
        if user_id is None:
            return jsonify({"error": "Valid user_id parameter is required"}), 400

        # Fetch subjects from SubjectManager
        subjects = []
        print("user_id", user_id, type (user_id))
        subjects = SubjectManager.get_all_with_details(int(user_id))

        # # Convert subjects to JSON format
        # subjects_data = [Subject(
        #     id=subject["subject_id"],
        #     code_name=subject["code_name"],
        #     difficulty=subject["difficulty"],
        #     user_id=subject["user_id"]
        # ).to_dict() for subject in subjects]

        # print("Fetched Subjects:", subjects_data)  # Debugging log
        return jsonify(subjects)
    
    except Exception as e:
        print("Error retrieving subjects:", str(e))  # Log error for debugging
        return jsonify({"error": str(e)}), 500

@study_routes.route("/subject/get_quests", methods=["GET"])
def get_subject_quests():
    subject_id = request.args.get("subject_id")  # ✅ Get subject ID from query params

    if not subject_id:
        return jsonify({"error": "Subject ID is required"}), 400

    try:
        # Convert subject_id to an integer safely
        subject_id = int(subject_id)
        
        # Fetch quests using SubjectManager
        quests = SubjectManager.get_quests(subject_id)

        # Ensure response is JSON serializable
        quests_data = [quest.to_dict() for quest in quests]  
        return jsonify(quests_data)

    except ValueError:
        return jsonify({"error": "Invalid Subject ID format"}), 400  # Handles non-integer input

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

        # Fetch and convert flashcards
        flashcards = SubjectManager.get_flashcards(subject_id) or []  # Ensure it's a list
        flashcards = [flashcard.to_dict() for flashcard in flashcards]

        return jsonify(flashcards)

    except ValueError:
        return jsonify({"error": "Invalid Subject ID format"}), 400  # Handles non-integer subject_id

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@study_routes.route("/subject/get_notes", methods=["GET"])
def get_subject_notes():
    subject_id = request.args.get("subject_id")  # ✅ Get subject ID from query params

    print("subject_id", request.args)

    if not subject_id:
        return jsonify({"error": "Subject ID is required"}), 400

    try:
        # Convert subject_id to int (assuming IDs are integers)
        subject_id = int(subject_id)

        # Fetch and convert flashcards
        notes = SubjectManager.get_notes(subject_id) or []  # Ensure it's a list        
        notes = [note.to_dict() for note in notes]

        return jsonify(notes)

    except ValueError:
        return jsonify({"error": "Invalid Subject ID format"}), 400  # Handles non-integer subject_id

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@study_routes.route("/quest/create", methods=["POST"])
def create_quest():
    try:
        # Get JSON or form data safely
        data = request.get_json(silent=True) or request.form

        # Validate required fields
        description = data.get("description", "").strip()
        difficulty = data.get("difficulty")
        subject_id = data.get("subject_id")

        if not description:
            return jsonify({"error": "Description is required"}), 400
        if difficulty is None or subject_id is None:
            return jsonify({"error": "Difficulty and subject_id are required"}), 400
        
        # Convert to correct types
        try:
            difficulty = int(difficulty)
            subject_id = int(subject_id)
        except ValueError:
            return jsonify({"error": "Invalid data type for difficulty or subject_id"}), 400

        # Create the new quest
        newQuest: Quest = QuestManager.create_quest(description=description, difficulty=difficulty, subject_id=subject_id)

        # Log for debugging
        print(f"✅ New Quest Created: {newQuest.to_dict()}")

        return jsonify({"quest": newQuest.to_dict()}), 201  # Use 201 for resource creation

    except Exception as e:
        print(f"❌ Error creating quest: {str(e)}")  # Log error
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@study_routes.route("/quest/get_by_subject_id", methods=["GET"])
def get_quest_by_subject_id():
    try:
        subject_id = request.args.get('subject_id', type=int)
        if not subject_id:
            return jsonify({"error": "subject_id parameter is required"}), 400
            
        quests = QuestManager.get_quests_by_subject(subject_id)
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
