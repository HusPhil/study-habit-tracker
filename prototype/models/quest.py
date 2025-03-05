from models.trackable_content import TrackableContent
from datetime import datetime

class Quest(TrackableContent):
    def __init__(self, description: str = "New Quest", subject=None, status: bool = False, difficulty: str = "easy"):
        super().__init__(description, subject, status, difficulty)
        self.completed_at = None

    def complete(self):
        """Mark the quest as completed"""
        self.status = True
        self.completed_at = datetime.now()
        if self.subject:
            self.subject.record_quest_completion(self)

    def uncomplete(self):
        """Mark the quest as not completed"""
        self.status = False
        self.completed_at = None

    def create(self) -> 'Quest':
        """Create a new quest instance"""
        return Quest(
            description=self.description,
            subject=self.subject,
            status=self.status,
            difficulty=self.difficulty,
        )

    def to_dict(self) -> dict:
        """Convert quest to dictionary for serialization"""
        return {
            'description': self.description,
            'status': self.status,
            'difficulty': self.difficulty,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }