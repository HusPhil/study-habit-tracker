from models.database.db import db, DatabaseError

class QuestManager:
    """Handles all database operations related to Quests."""

    @staticmethod
    def create(description: str, difficulty: int, subject_id: int) -> dict:
        """Create a new quest in the database and return its details."""
        try:
            existing_quest = db.execute(
                "SELECT * FROM quests WHERE description = ? AND subject_id = ?", 
                (description, subject_id)
            )
            if existing_quest:
                return existing_quest[0]  # Return existing quest as a dict

            # Insert the new quest
            db.execute(
                "INSERT INTO quests (description, difficulty, subject_id, status) VALUES (?, ?, ?, ?)",
                (description, difficulty, subject_id, 0)
            )

            # Retrieve the newly created quest
            result = db.execute("SELECT * FROM quests WHERE description AND subject_id = ?", (description, subject_id))
            if result:
                return result[0]  # Return new quest data as a dict

            raise DatabaseError("Failed to create quest")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating quest: {str(e)}")

    @staticmethod
    def get_quests_by_subject(subject_id: int) -> list:
        """Fetch all quests for a subject and return them as a list of dictionaries."""
        try:
            result = db.execute("SELECT * FROM quests WHERE subject_id = ?", (subject_id,))
            return result  # Return list of quest dictionaries
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving quests: {str(e)}")
