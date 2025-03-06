from flask import Blueprint, request, jsonify, redirect, url_for
from typing import Dict
from models import Subject, Quest  # Import the Subject model


study_routes = Blueprint("study_routes", __name__)  # Define Blueprint

# Start Session Route
@study_routes.route("/start_session", methods=["POST"])
def start_session():
    try:
        data: Dict = request.get_json()
        print("Received Data:", data)

        return jsonify({
            "message": "Session started successfully",
            "data": data
        })
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

@study_routes.route("/quest/create", methods=["POST"])
def create_quest():
    try:
        data: Dict = request.get_json()
        
        if not all(key in data for key in ["description", "difficulty", "subject_id"]):
            return jsonify({"error": "Missing required fields"}), 400

        newQuest = Quest.create(
            description=data["description"],
            difficulty=data["difficulty"],
            subject_id=data["subject_id"]
        )

        return jsonify({
            "message": "Quest created successfully",
            "quest": newQuest.to_dict(),
            "status": 200
        })
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
