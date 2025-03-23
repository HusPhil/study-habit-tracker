from models.database.db import db, DatabaseError

class BadgeManager:
    """Handles database operations for Notes."""

    @staticmethod
    def create(title: str, rarity: str, user_id: int) -> dict:
        """Create a new note in the database and return its details."""
        try:
            already_have_badge = db.execute(
                "SELECT * FROM badges WHERE user_id = ?", 
                (user_id)
            ) 

            if already_have_badge:
                return already_have_badge[0]

            db.execute(
                "INSERT INTO badges (title, rarity) VALUES (?, ?)",
                (title, rarity)
            )
            
            result = db.execute(
                "SELECT * FROM badges WHERE user_id = ?", 
                (user_id)
            ) 

            if result:
                return dict(result[0])
            
            raise DatabaseError("Failed to create note")
        
        except DatabaseError as e:
            raise DatabaseError(f"Error creating note: {str(e)}")
