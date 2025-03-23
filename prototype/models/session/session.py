from flask_socketio import SocketIO
from .session_manager import SessionManager
from models.subject.subject_manager import SubjectManager


class Session:

    def __init__(self, id: int, duration: int, subject_id: int, goals):
        self._id = id
        self._subject_id = subject_id
        self._duration = duration
        self._accumulated_exp = 0
        self.goals = goals

    def start(self, user_id: int, socketio):
        """Start the session using session_manager with safety checks."""

        if self._validate_session(user_id, socketio, "start"):
            return self._validate_session(user_id, socketio, "start")

        try:
            result = SessionManager.start_session(
                session=self, 
                user_id=user_id, 
                socketio=socketio
            )
            
            if user_id not in SessionManager.active_sessions:
                return {"error": "Session failed to startss"}
            
            subject_data = SubjectManager.get(self.subject_id)
            self.accumulated_exp = (int(subject_data["difficulty"]) * self.duration) // 10
            
            return result
        except Exception as e:
            return {"error": f"Failed to start session: {str(e)}"}

    def stop(self, user_id: int, socketio):
        """Stop the session using session_manager with safety checks."""

        if self._validate_session(user_id, socketio, "stop"):
            return self._validate_session(user_id, socketio, "stop")
        
        try:
            result = SessionManager.stop_session(self.id, user_id, socketio)
            
            if self.id in SessionManager.active_sessions:
                return {"error": "Session failed to stop properly"}

            return {**result, "selected_quests": self.goals, "subject_id": self.subject_id} 
        except Exception as e:
            return {"error": f"Failed to stop session: {str(e)}"}
        
    def _validate_session(self, user_id, socketio, action: str) -> dict:
        """Validate session conditions for starting or stopping a session.
        
        Args:
            user_id (int): The ID of the user.
            socketio (SocketIO): The SocketIO instance.
            action (str): Either 'start' or 'stop' to determine validation logic.

        Returns:
            dict | None: A dictionary with an error message if validation fails, or None if valid.
        """
        
        errors = {
            "id": "Invalid session: Missing session ID" if not self.id else None,
            "duration": "Session duration must be a positive integer" 
                        if not isinstance(self.duration, int) or self.duration <= 0 else None,
            "goals": "Goals must be a list" if not isinstance(self.goals, list) else None,
            "socketio": "SocketIO instance is required" if socketio is None else None,
        }
        
        if action == "start":
            errors["duplicate"] = f"A session {self.id} is already running" if user_id in SessionManager.active_sessions else None
        elif action == "stop":
            errors["not_active"] = "No active session found for this user" if user_id not in SessionManager.active_sessions else None

        # Filter out None values and return the first error found
        return { "error": next((msg for msg in errors.values() if msg), None) } if any(errors.values()) else None

    
    @property
    def id(self):
        return self._id
    
    @property
    def subject_id(self):
        return self._subject_id
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def accumulated_exp(self):
        return self._accumulated_exp    
    
    @accumulated_exp.setter
    def accumulated_exp(self, value):
        self._accumulated_exp = value