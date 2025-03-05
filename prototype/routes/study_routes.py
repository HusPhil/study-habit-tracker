from flask import Blueprint, request, jsonify
from typing import Dict

study_routes = Blueprint("study_routes", __name__)  # ✅ Define Blueprint

# ✅ Start Session Route
@study_routes.route("/start_session", methods=["POST"])
def start_session():
    try:
        data: Dict = request.get_json()  # ✅ Correct way to parse JSON
        print("Received Data:", data)  # Debugging print

        return jsonify({
            "message": "Session started successfully",
            "data": data  # ✅ Send parsed data back as JSON
        })
    except Exception as e:
        return jsonify({"error": f"Invalid request: {str(e)}"}), 400
