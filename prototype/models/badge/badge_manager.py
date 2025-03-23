from models.database.db import db, DatabaseError

class BadgeManager:
    """Handles database operations for Notes."""

    @staticmethod
    def create(title: str, rarity: str, user_id: int) -> dict:
        """Create a new badge in the database and return its details."""
        try:
            # Check if the user already has a badge
            already_have_badge = db.execute("SELECT * FROM badges WHERE user_id = ?", (user_id,))
            if already_have_badge:
                return dict(already_have_badge[0])  # Convert result to dictionary

            # Insert the new badge
            db.execute(
                "INSERT INTO badges (title, rarity, user_id) VALUES (?, ?, ?)",
                (title, rarity, user_id)
            )

            # Retrieve the newly created badge
            new_badge = db.execute("SELECT * FROM badges WHERE user_id = ? ORDER BY badge_id DESC LIMIT 1", (user_id,))
            if new_badge:
                return dict(new_badge[0])

            raise DatabaseError("Failed to create badge")

        except Exception as e:
            raise DatabaseError(f"Error creating badge: {str(e)}")
