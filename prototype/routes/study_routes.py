from flask import Blueprint, request, jsonify, redirect, url_for
from typing import Dict
from models import Subject, Quest  # Import the Subject model
from models.enemy import EnemyType

study_routes = Blueprint("study_routes", __name__)  # Define Blueprint

# Start Session Route
@study_routes.route("/start_session", methods=["POST"])
def start_session():
    try:
        data = request.json
        subject = Subject.get(data["subject_id"])
        selected_quests: list = data["selected_quests"]
        enemies: list[EnemyType] = subject.spawnEnemy(len(selected_quests))

        for enemy in enemies:
            print(f"Enemy: {enemy.value}")

        return jsonify({"message": "Session started successfully"})
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400

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
        newSubject = Subject.create(
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
