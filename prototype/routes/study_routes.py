from flask import Blueprint, request, jsonify, redirect, url_for, session, abort
from typing import Dict
from models import Subject, Quest, Session  # Import the Subject model
from models.enemy.enemy import Enemy

from models.player.player import Player
from models.player.player_manager import PlayerManager

from models.session.session import SessionManager

from models.subject.subject_manager import SubjectManager
from models.quest.quest_manager import QuestManager

from models.note.note import Note
from models.note.note_manager import NoteManager

from models.flashcard.flashcard import Flashcard
from models.flashcard.flashcard_manager import FlashcardManager

from models.badge.badge_manager import BadgeManager

from extensions import socketio
import time, logging

study_routes = Blueprint("study_routes", __name__)  # Define Blueprint

# Start Session Route
@study_routes.route("/start_session", methods=["POST"])
def start_session():
    try:
        print("START SESSION")

        data = request.get_json()
        
        subject_data = SubjectManager.get(data["subject_id"])
        subject: Subject = Subject(id=subject_data["subject_id"], code_name=subject_data["code_name"], difficulty=subject_data["difficulty"], user_id=subject_data["user_id"])
        if not subject:
            print("Subject not found")
            return jsonify({"error": "Subject not found"}), 404
        
        selected_quests: list = data["selected_quests"]
        battle_duration_mins = int(data["battle_duration"])
        user_id = data["user_id"]

        enemies: list[Enemy] = subject.spawn_enemies(selected_quests)  
        print("enemies", enemies)
        
        session = Session(
            id=int(time.time()), 
            subject_id=subject.id, 
            duration=battle_duration_mins, 
            goals=selected_quests
        )
        
        if session.id in SessionManager.active_sessions:
            return jsonify("Session already started")

        session_data = session.start(user_id=int(user_id), socketio=socketio)

        print("enemies", enemies, session_data)

        return jsonify({
            "session_data": session_data, 
            "enemies": [enemy.to_dict() for enemy in enemies],
        })

        raise NotImplementedError
    
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

@study_routes.route("/stop_session", methods=["POST"])
def stop_session():
    """Stops an active study session and processes rewards."""
    try:
        user_id = session.get("user_id")  # Ensure we get an integer user_id
        if user_id is None:
            return error_response("User ID not found in session", 400)

        current_session: Session = SessionManager.active_sessions.get(user_id)
        if not current_session:
            return error_response("No active session found for this user", 404)

        session_data = current_session.stop(user_id=user_id, socketio=socketio)
        data = request.get_json() or {}  # Ensure we have a valid dictionary
        
        remaining_enemies = data.get("remaining_enemies")
        total_enemies = data.get("total_enemies")

        if remaining_enemies is None or total_enemies is None:
            return error_response("Missing enemy count data", 400)

        player = Player(**PlayerManager.get(user_id))
        logging.info(f"Stopping session for user {user_id}, Accumulated EXP: {current_session.accumulated_exp}")

        adventurer_badge = None
        # Badge reward for new players
        if player.exp <= 0 and player.level <= 1:
            adventurer_badge = Enemy.drop_badge({"title": "Novice Adventurer", "rarity": "Common"})
            BadgeManager.create(user_id=user_id, rarity=adventurer_badge.rarity, title=adventurer_badge.title)

        # Calculate experience gain
        exp_data = PlayerManager.calculate_exp(total_enemies=total_enemies, remaining_enemies=remaining_enemies)
        player.gain_exp(exp_data["net_exp"])

        # If all enemies are defeated, complete quests
        if remaining_enemies <= 0:
            complete_quests(player, session_data, current_session)

        # Save updated player data
        PlayerManager.save(player.to_dict())

        return jsonify({
            "message": "Session stopped successfully",
            "player_stats": player.to_dict(),
            "default_badge": adventurer_badge.to_string() if adventurer_badge else None, 
            "subject_id": session_data.get("subject_id")
        })
    
    except Exception as e:
        logging.error(f"Error stopping session: {str(e)}", exc_info=True)
        return error_response("An unexpected error occurred", 500)


def complete_quests(player, session_data, current_session):
    """Handles quest completion logic when all enemies are defeated."""
    selected_quests = session_data.get("selected_quests", [])
    quest_ids = [quest["id"] for quest in selected_quests if "id" in quest]
    
    if quest_ids:
        player.gain_exp(current_session.accumulated_exp)
        QuestManager.delete_quests(quest_ids)


def error_response(message, status_code):
    """Helper function to return standardized error responses."""
    return jsonify({"error": message}), status_code
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
        data = request.form

        print(data)

        # Validate required fields
        description = data["description"].strip()
        difficulty = data["questDifficulty"]
        subject_id = data["subject_id"]

        if not description:
            print("Description is required")
            return jsonify({"error": "Description is required"}), 400
        if difficulty is None or subject_id is None:
            print("Difficulty and subject_id are required")
            return jsonify({"error": "Difficulty and subject_id are required"}), 400
        
        # Convert to correct types
        try:
            difficulty = int(difficulty)
            subject_id = int(subject_id)
        except ValueError:
            return jsonify({"error": "Invalid data type for difficulty or subject_id"}), 400

        # Create the new quest

        newQuest_data = QuestManager.create(description=description, difficulty=difficulty, subject_id=subject_id)

        newQuest = Quest(id=newQuest_data["quest_id"],
                         description=newQuest_data["description"], subject_id=newQuest_data["subject_id"], 
                         status=newQuest_data["status"], difficulty=newQuest_data["difficulty"])
        print(newQuest)

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


@study_routes.route("/note/create", methods=["POST"])
def create_note():
    try:
        # Get JSON or form data safely
        data = request.form

        print(data)

        # Validate required fields
        description = data["note_description"].strip()
        link = data["note_link"]
        subject_id = data["subject_id"]

        if not description:
            print("Description is required")
            return jsonify({"error": "Description is required"}), 400
        if link is None or subject_id is None:
            print("Difficulty and subject_id are required")
            return jsonify({"error": "Difficulty and subject_id are required"}), 400
        
        # Convert to correct types
        try:
            subject_id = int(subject_id)
        except ValueError:
            return jsonify({"error": "Invalid data type for difficulty or subject_id"}), 400

        # Create the new quest

        newNote_data = NoteManager.create(description=description, link=link, subject_id=subject_id)
        #  id: int, description: str, subject_id: int, link

        newNote = Note(id=newNote_data["note_id"], description=newNote_data["description"], 
                        subject_id=newNote_data["subject_id"], link=newNote_data["link"],)
        print(newNote)

        # Log for debugging
        print(f"✅ New Note Created: {newNote.to_dict()}")

        return jsonify({"note": newNote.to_dict()}), 201  # Use 201 for resource creation

    except Exception as e:
        print(f"❌ Error creating note: {str(e)}")  # Log error
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


@study_routes.route("/flashcard/create", methods=["POST"])
def create_flashcard():
    try:
        # Get JSON or form data safely
        data = request.form

        print(data)

        # Validate required fields
        description = data["flashcard_description"].strip()
        link = data["flashcard_link"]
        subject_id = data["subject_id"]

        if not description:
            print("Description is required")
            return jsonify({"error": "Description is required"}), 400
        if link is None or subject_id is None:
            print("Difficulty and subject_id are required")
            return jsonify({"error": "Difficulty and subject_id are required"}), 400
        
        # Convert to correct types
        try:
            subject_id = int(subject_id)
        except ValueError:
            return jsonify({"error": "Invalid data type for difficulty or subject_id"}), 400

        # Create the new quest

        newFlashcard_data = FlashcardManager.create(description=description, link=link, subject_id=subject_id)
        #  id: int, description: str, subject_id: int, link

        newFlashcard = Flashcard(id=newFlashcard_data["flashcard_id"], description=newFlashcard_data["description"], 
                        subject_id=newFlashcard_data["subject_id"], link=newFlashcard_data["link"],)
        print(newFlashcard)

        # Log for debugging
        print(f"✅ New Note Created: {newFlashcard.to_dict()}")

        return jsonify({"note": newFlashcard.to_dict()}), 201  # Use 201 for resource creation

    except Exception as e:
        print(f"❌ Error creating note: {str(e)}")  # Log error
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# @study_routes.route("/player/get_stats", methods=["POST"])
# def get_player_stats():    
#     try:
        
