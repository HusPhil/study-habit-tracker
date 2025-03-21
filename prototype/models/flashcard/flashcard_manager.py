from models.database.db import db, DatabaseError

class FlashcardManager:
    """Handles database operations for Flashcards."""

    @staticmethod
    def create(subject_id: int, description: str, link: str) -> dict:
        """Create a new flashcard in the database or return an existing one as a dictionary."""
        try:
            # Check if flashcard already exists
            existing_flashcard = db.execute("SELECT * FROM flashcards WHERE link = ?", (link,))
            if existing_flashcard:
                return dict(existing_flashcard[0])  # ✅ Return existing flashcard
            
            # Insert new flashcard
            db.execute(
                "INSERT INTO flashcards (subject_id, description, link) VALUES (?, ?, ?)",
                (subject_id, description, link)
            )

            # Retrieve the newly created flashcard using LAST_INSERT_ROWID()
            result = db.execute("SELECT * FROM flashcards WHERE flashcard_id = LAST_INSERT_ROWID()")
            return dict(result[0]) if result else None
        
        except DatabaseError as e:
            raise DatabaseError(f"Error creating flashcard: {str(e)}")
