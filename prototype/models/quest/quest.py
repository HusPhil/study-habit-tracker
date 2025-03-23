from models.content.trackable_content import TrackableContent
from models.database.db import db

class Quest(TrackableContent):
    def __init__(self, id: int = None, description: str = "New Quest", 
                 subject_id: int = None, status: int = 0, 
                 difficulty: int = 3):
        super().__init__(description, subject_id, status, difficulty)
        self._id = id
        self._difficulty = difficulty
  
    def to_dict(self) -> dict:
        """Convert quest to dictionary for serialization"""
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'description': self.description,
            'status': self.status,
            'difficulty': self.difficulty,
        }
    
    @property
    def difficulty(self):
        return self._difficulty


    @property
    def id(self):
        return self._id