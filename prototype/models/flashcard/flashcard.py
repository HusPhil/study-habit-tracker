from models.trackable_content import TrackableContent
from models.db import db

class Flashcard(TrackableContent):
    """Represents a flashcard with tracking capabilities."""

    def __init__(self, id=None, question="", answer="", subject_id=None, 
                 status=False, difficulty="Easy"):
        super().__init__(status=status, difficulty=difficulty)
        self.id = id
        self.question = question
        self.answer = answer
        self.subject_id = subject_id  

    @classmethod
    def create(cls, question: str, answer: str, subject_id: int, difficulty: str = "Easy") -> 'Flashcard':
        """Creates and stores a new flashcard in the database."""
        query = """
        INSERT INTO flashcards (question, answer, subject_id, status, difficulty) 
        VALUES (?, ?, ?, ?, ?) RETURNING id
        """
        try:
            result = db.execute(query, (question, answer, subject_id, False, difficulty))
            db.commit()
            flashcard_id = result[0]['id'] if result else None
            return cls(id=flashcard_id, question=question, answer=answer, 
                       subject_id=subject_id, status=False, difficulty=difficulty)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error creating flashcard: {e}")

    @classmethod
    def get_all(cls):
        """Retrieves all flashcards from the database."""
        query = "SELECT * FROM flashcards"
        return [cls(**data) for data in db.fetch_all(query)]

    @classmethod
    def get_by_id(cls, flashcard_id: int) -> 'Flashcard | None':
        """Retrieves a single flashcard by its ID."""
        query = "SELECT * FROM flashcards WHERE id = ?"
        data = db.fetch_one(query, (flashcard_id,))
        return cls(**data) if data else None

    def update(self, question=None, answer=None, status=None, difficulty=None):
        """Updates the flashcard details in the database."""
        query = """
        UPDATE flashcards 
        SET question = ?, answer = ?, status = ?, difficulty = ? 
        WHERE id = ?
        """
        try:
            db.execute(query, (question or self.question, answer or self.answer, 
                               status if status is not None else self.status, 
                               difficulty or self.difficulty, self.id))
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error updating flashcard: {e}")

    @classmethod
    def delete(cls, flashcard_id: int):
        """Deletes a flashcard by ID."""
        query = "DELETE FROM flashcards WHERE id = ?"
        try:
            db.execute(query, (flashcard_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise Exception(f"Error deleting flashcard: {e}")
