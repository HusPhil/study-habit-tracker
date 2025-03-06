from models.trackable_content import TrackableContent
from .db import db

class Quest(TrackableContent):
    def __init__(self, id: int = None, description: str = "New Quest", 
                 subject_id: int = None, status: int = 0, 
                 difficulty: int = 1):
        super().__init__(description, subject_id, status, difficulty)
        self.id = id
        self.subject_id = subject_id
        self.description = description
        self.status = status
        self.difficulty = difficulty
    
    def to_dict(self) -> dict:
        """Convert quest to dictionary for serialization"""
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'description': self.description,
            'status': self.status,
            'difficulty': self.difficulty,
        }