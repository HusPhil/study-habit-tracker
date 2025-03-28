import time
from datetime import datetime, timedelta
from flask_socketio import SocketIO

class SessionManager:
    active_sessions = {}  # ✅ Store active sessions globally

    @staticmethod
    def start_session(session, user_id: int, socketio: SocketIO):
        """Start a session and store it in active_sessions."""
        
        SessionManager.active_sessions[user_id] = session  # ✅ Store session
        socketio.start_background_task(SessionManager.session_countdown, session.id, user_id, session.duration, socketio)

        return {
            "message": "Session started",
            "session_id": session.id,
            "user_id": user_id,
            "duration": session.duration,
        }

    @staticmethod
    def stop_session(session_id: int, user_id: int, socketio: SocketIO):
        """Stop a session and remove it from active_sessions."""

        session = SessionManager.active_sessions.pop(user_id, None)  # Remove from tracking
        
        if session:
            socketio.emit("session_ended", {"session_id": session_id})
            return {"message": "Session ended", "session_id": session_id}
        
        return {"error": "Session not found"}

    @staticmethod
    def session_countdown(session_id, user_id, duration, socketio):
        """Handles session countdown for a specific user"""
        for remaining in range(duration * 60, -1, -1):
            if user_id not in SessionManager.active_sessions:
                return  # Stop if session was canceled

            # Emit only to the specific user (using a "room")
            socketio.emit("session_update", 
                          {"session_id": session_id, 
                           "user_id": user_id, 
                           "time_left": remaining}, 
                           room=f"user_{user_id}")
            
            time.sleep(1)  # Wait 1 second

        # Notify only the specific user when the session ends
        socketio.emit("session_ended", {"user_id": user_id}, room=f"user_{user_id}")
        SessionManager.active_sessions.pop(user_id, None)  # Remove from active sessions
