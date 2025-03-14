from models.database.db import db, DatabaseError
from typing import Optional
from werkzeug.security import generate_password_hash


class PlayerManager:
    @staticmethod
    def create(email: str, username: str, password: str) -> dict:
        """Create a new player in the database or return an existing one as a dictionary."""
        try:
            existing_player = db.execute("SELECT * FROM users WHERE email = ?", (email,))
            if existing_player:
                return dict(existing_player[0])  # ✅ Return dictionary

            # Insert new player
            hashed_password = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (email, username, password, level, exp, title) VALUES (?, ?, ?, ?, ?, ?)",
                (email, username, hashed_password, 1, 0, "Noobie")
            )

            # Retrieve and return the newly created player
            result = db.execute("SELECT * FROM users WHERE email = ?", (email,))
            return dict(result[0]) if result else None
        except DatabaseError as e:
            raise DatabaseError(f"Error creating player: {str(e)}")

    @staticmethod
    def get(user_id: int) -> Optional[dict]:
        """Retrieve a player from the database as a dictionary."""
        try:
            result = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return dict(result[0]) if result else None
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving player: {str(e)}")

    @staticmethod
    def save(player_data: dict) -> None:
        """Save changes to the database for an existing player."""
        try:
            db.execute("""
                UPDATE users 
                SET email = ?, username = ?, password = ?, level = ?, exp = ?, title = ?
                WHERE user_id = ?
            """, (player_data["email"], player_data["username"], player_data["password"],
                  player_data["level"], player_data["exp"], player_data["title"], player_data["user_id"]))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving player: {str(e)}")

    @staticmethod
    def get_exp_threshold(level: int) -> int:
        """Get experience points needed for the next level."""
        return level * 100

    @staticmethod
    def gain_exp(user_id: int, amount: int) -> None:
        """Increase player's experience and level up if necessary."""
        player_data = PlayerManager.get(user_id)
        if not player_data:
            raise DatabaseError("Player not found")

        player_data["exp"] += amount
        while player_data["exp"] >= PlayerManager.get_exp_threshold(player_data["level"]):
            # ✅ Use `level_up()` method in Player
            player = Player(**player_data)  # Convert dict to Player object
            player.level_up()
            player_data.update(player.to_dict())  # Update player data dictionary

        PlayerManager.save(player_data)
