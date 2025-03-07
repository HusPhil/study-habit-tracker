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
    
    @staticmethod
    def create(description: str, difficulty: int, subject_id: int) -> 'Quest':
        """Create a new quest in database"""
        try:
            existing_quest = db.execute("SELECT * FROM quests WHERE description = ?", (description,))
            if existing_quest:
                # If it exists, return the existing quest
                data = existing_quest[0]
                return Quest(
                    id=data['quest_id'],
                    description=data['description'],
                    subject_id=data['subject_id'],
                    status=data['status'],
                    difficulty=data['difficulty']
                )
            # Insert the quest data
            db.execute(
                "INSERT INTO quests (description, difficulty, subject_id, status) VALUES (?, ?, ?, ?)",
                (description, difficulty, subject_id, 0)
            )
            
            # Get the created quest
            result = db.execute("SELECT * FROM quests WHERE description = ?", (description,))
            if result:
                data = result[0]
                return Quest(
                    id=data['quest_id'],
                    description=data['description'],
                    subject_id=data['subject_id'],
                    status=data['status'],
                    difficulty=data['difficulty']
                )
            raise DatabaseError("Failed to create quest")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating quest: {str(e)}")

    @staticmethod
    def get_by_subject_id(subject_id: int) -> list['Quest']:
        """Get all quests by subject_id"""
        try:
            result = db.execute("SELECT * FROM quests WHERE subject_id = ?", (subject_id,))
            return [Quest(
                id=data['quest_id'],
                description=data['description'],
                subject_id=data['subject_id'],
                status=data['status'],
                difficulty=data['difficulty']
            ) for data in result]
        except DatabaseError as e:
            raise DatabaseError(f"Error getting quests by subject_id: {str(e)}")

    def to_dict(self) -> dict:
        """Convert quest to dictionary for serialization"""
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'description': self.description,
            'status': self.status,
            'difficulty': self.difficulty,
        }