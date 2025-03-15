from flask_socketio import SocketIO
from .session_manager import SessionManager

class Session:

    def __init__(self, id: int, duration: int, subject_id: int, goals):
        self.id = id
        self.subject_id = subject_id
        self.duration = duration
        self.goals = goals
        self.accumulated_exp = 0

    def start(self, user_id: int, socketio):
        """Start the session using session_manager with safety checks."""

        if not self.id:
            return {"error": "Invalid session: Missing session ID"}
        
        if user_id in SessionManager.active_sessions:
            return {"error": f"A session {self.id} is already running"}

        if not isinstance(self.duration, int) or self.duration <= 0:
            return {"error": "Session duration must be a positive integer"}

        if not isinstance(self.goals, list):
            return {"error": "Goals must be a list"}

        if socketio is None:
            return {"error": "SocketIO instance is required"}

        try:
            result = SessionManager.start_session(session=self, user_id=user_id, socketio=socketio)
            
            if user_id not in SessionManager.active_sessions:
                return {"error": "Session failed to startss"}
            
            return result
        except Exception as e:
            return {"error": f"Failed to start session: {str(e)}"}

    def stop(self, user_id: int, socketio):
        """Stop the session using session_manager with safety checks."""
        
        if not self.id:
            return {"error": "Invalid session: Missing session ID"}

        # if self.id not in SessionManager.active_sessions:
        #     return {"error": f"Session {self.id} is not active or has already ended"}

        if socketio is None:
            return {"error": "SocketIO instance is required"}

        try:
            result = SessionManager.stop_session(self.id, user_id, socketio)
            
            if self.id in SessionManager.active_sessions:
                return {"error": "Session failed to stop properly"}

            return result 
        except Exception as e:
            return {"error": f"Failed to stop session: {str(e)}"}
        
    def get_session_status(self):
        """Get the status of the session."""
        if self.id not in SessionManager.active_sessions:
            return {"error": f"Session {self.id} is not active or has already ended"}
        return {"status": "active"}
