from models.db import db
from models.flashcard import Flashcard

class FlashcardManager:
    """Handles database operations for Flashcards."""

    @classmethod
    def create(cls, link: str) -> Flashcard:
        """Creates and stores a new flashcard in the database."""
        query = "INSERT INTO flashcards (link) VALUES (?) RETURNING id"
        try:
            result = db.execute(query, (link,))
            db.commit()
            return Flashcard(link=link)
        except Exception as e:
            db.rollback()
            raise Exception(f"Error creating flashcard: {e}")

    @classmethod
    def get_all(cls):
        """Retrieves all flashcards from the database."""
        query = "SELECT * FROM flashcards"
        return [Flashcard(**data) for data in db.fetch_all(query)]

    @classmethod
    def get_by_id(cls, flashcard_id: int) -> Flashcard | None:
        """Retrieves a single flashcard by its ID."""
        query = "SELECT * FROM flashcards WHERE id = ?"
        data = db.fetch_one(query, (flashcard_id,))
        return Flashcard(**data) if data else None

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
