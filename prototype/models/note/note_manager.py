from models.db import db
from models.note import Note

class NoteManager:
    """Handles database operations for Notes."""

    @classmethod
    def create(cls, link: str) -> Note:
        """Creates and stores a new Note in the database."""
        query = "INSERT INTO notes (link) VALUES (?) RETURNING id"
        try:
            result = db.execute(query, (link,))
            db.commit()
            return Note(link=link)
        except Exception as e:
            db.rollback()
            raise RuntimeError(f"Error creating note: {e}")
