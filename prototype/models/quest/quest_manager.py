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
            result = db.execute("SELECT * FROM quests WHERE description = ? AND subject_id = ?", (description, subject_id))
            print(result)
            if result:
                return result[0]  # Return new quest data as a dict

            raise DatabaseError("Failed to create quest")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating quest: {str(e)}")

    @staticmethod
    def delete(id: int) -> dict:
        """Delete a quest from the database and return confirmation."""
        try:
            # Check if the quest exists
            existing_quest = db.execute("SELECT * FROM quests WHERE id = ?", (id,))
            if not existing_quest:
                raise DatabaseError(f"Quest with id {id} not found")

            # Delete the quest
            db.execute("DELETE FROM quests WHERE id = ?", (id,))

            return {"message": f"Quest with id {id} deleted successfully"}
        
        except DatabaseError as e:
            raise DatabaseError(f"Error deleting quest: {str(e)}")

    @staticmethod
    def delete_quests(ids: list[int]) -> dict:
        """Delete multiple quests from the database and return confirmation."""
        try:
            if not ids:
                raise ValueError("Quest ID list cannot be empty")

            # Convert list of IDs to a format that SQL can process (tuple)
            placeholders = ", ".join("?" * len(ids))

            # Check if the quests exist
            existing_quests = db.execute(f"SELECT quest_id FROM quests WHERE quest_id IN ({placeholders})", tuple(ids))
            if not existing_quests:
                raise DatabaseError("No matching quests found for deletion")

            # Delete the quests
            db.execute(f"DELETE FROM quests WHERE quest_id IN ({placeholders})", tuple(ids))

            return {"message": f"Deleted {len(existing_quests)} quest(s) successfully"}
        
        except DatabaseError as e:
            raise DatabaseError(f"Error deleting quests: {str(e)}")

    @staticmethod
    def get_quests_by_subject(subject_id: int) -> list:
        """Fetch all quests for a subject and return them as a list of dictionaries."""
        try:
            result = db.execute("SELECT * FROM quests WHERE subject_id = ?", (subject_id,))
            return result  # Return list of quest dictionaries
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving quests: {str(e)}")
