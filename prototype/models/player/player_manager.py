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
                SET level = ?, exp = ?, title = ?
                WHERE user_id = ?
            """, (player_data["level"], player_data["exp"], player_data["title"], player_data["user_id"]))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving player: {str(e)}")

    @staticmethod
    def get_exp_threshold(level: int) -> int:
        """Calculate experience points needed for the next level."""
        base_exp = 100  # Base XP required at level 1
        exponent = 1.5  # Growth rate (adjustable)

        return int(base_exp * (level ** exponent))
    
    @staticmethod
    def calculate_exp(total_enemies: int, remaining_enemies: int, base_exp_per_enemy: int = 50):
        """
        Calculates experience gain and loss based on defeated and remaining enemies.

        :param total_enemies: Total number of enemies in the battle.
        :param remaining_enemies: Number of enemies left when the battle ends.
        :param base_exp_per_enemy: Base EXP awarded per enemy.
        :return: Dictionary containing final EXP gain and loss.
        """

        # Ensure valid values to prevent errors
        total_enemies = max(1, total_enemies)  # Prevent division by zero
        remaining_enemies = max(0, min(remaining_enemies, total_enemies))  # Ensure within valid range

        # Total possible EXP if all enemies are defeated
        total_exp = base_exp_per_enemy * total_enemies

        # EXP gained based on number of defeated enemies
        defeated_enemies = total_enemies - remaining_enemies
        exp_gain = (total_exp / total_enemies) * defeated_enemies  

        # Full clear bonus (extra 10% if all enemies are defeated)
        if remaining_enemies == 0:
            exp_gain *= 1.1  

        # EXP loss for remaining enemies (50% of their potential EXP)
        exp_loss = (base_exp_per_enemy * remaining_enemies) / 2 if remaining_enemies > 0 else 0

        return {
            "exp_gain": round(exp_gain),
            "exp_loss": round(exp_loss),
            "net_exp": round(exp_gain - exp_loss)  # Final EXP after loss is considered
        }
    


    
