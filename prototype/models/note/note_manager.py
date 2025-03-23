from models.database.db import db, DatabaseError

class NoteManager:
    """Handles database operations for Notes."""

    @staticmethod
    def create(description: str, link: int, subject_id: int) -> dict:
        """Create a new note in the database and return its details."""
        try:
            existing_note = db.execute(
                "SELECT * FROM notes WHERE description = ? AND subject_id = ?", 
                (description, subject_id)
            )
            if existing_note:
                return existing_note[0]  # Return existing note as a dict

            # Insert the new note
            db.execute(
                "INSERT INTO notes (description, link, subject_id) VALUES (?, ?, ?)",
                (description, link, subject_id)
            )

            # Retrieve the newly created note
            result = db.execute("SELECT * FROM notes WHERE description = ? AND subject_id = ?", (description, subject_id))
            print(result)
            if result:
                return result[0]  # Return new note data as a dict

            raise DatabaseError("Failed to create note")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating note: {str(e)}")
