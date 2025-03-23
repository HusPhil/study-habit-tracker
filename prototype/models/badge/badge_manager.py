from models.database.db import db, DatabaseError

class BadgeManager:
    """Handles database operations for Notes."""
    
    @staticmethod
    def create(title: str, rarity: str, description: str, user_id: int) -> dict:
        """Create a new badge in the database and return its details."""
        try:
            # Check if the user already has a badge
            already_have_badge = db.execute("SELECT * FROM badges WHERE user_id = ?", (user_id,))
            if already_have_badge and len(already_have_badge) > 0:
                return dict(already_have_badge[0])  # Convert first result to dictionary

            # Insert the new badge
            db.execute(
                "INSERT INTO badges (title, rarity, description, user_id) VALUES (?, ?, ?, ?)",
                (title, rarity, description, user_id)  # ✅ Corrected placeholders
            )

            # Retrieve the newly created badge
            new_badge = db.execute("SELECT * FROM badges WHERE user_id = ? ORDER BY badge_id DESC LIMIT 1", (user_id,))
            if new_badge and len(new_badge) > 0:
                return dict(new_badge[0])

            raise DatabaseError("Failed to create badge")

        except Exception as e:
            raise DatabaseError(f"Error creating badge: {str(e)}")


    def get_user_badges(user_id: int) -> list[dict]:
        try:
            badges = db.execute("SELECT * FROM badges WHERE user_id = ?", (user_id,))
            return [dict(badge) for badge in badges]

        except Exception as e:
            raise DatabaseError(f"Error getting user badges: {str(e)}")