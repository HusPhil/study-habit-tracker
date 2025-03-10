from models.database.db import db, DatabaseError
from models.player.player import Player
from typing import Optional
from werkzeug.security import generate_password_hash

class PlayerManager:
    @staticmethod
    def create(email: str, username: str, password: str) -> Player:
        """Create a new player in the database or return an existing one."""
        try:
            existing_player = db.execute("SELECT * FROM users WHERE email = ?", (email,))
            if existing_player:
                data = existing_player[0]
                return Player(
                    user_id=data['user_id'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                    level=data['level'],
                    exp=data['exp'],
                    title=data['title']
                )

            # Insert new player
            hashed_password = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (email, username, password, level, exp, title) VALUES (?, ?, ?, ?, ?, ?)",
                (email, username, hashed_password, 1, 0, "Noobie")
            )

            # Retrieve the newly created player
            result = db.execute("SELECT * FROM users WHERE email = ?", (email,))
            if result:
                data = result[0]
                return Player(
                    user_id=data['user_id'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                    level=data['level'],
                    exp=data['exp'],
                    title=data['title']
                )

            raise DatabaseError("Failed to create player")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating player: {str(e)}")

    @staticmethod
    def get(user_id: int) -> Optional[Player]:
        """Retrieve a player from the database."""
        try:
            result = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            if result:
                data = result[0]
                return Player(
                    user_id=data['user_id'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                    level=data['level'],
                    exp=data['exp'],
                    title=data['title']
                )
            return None
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving player: {str(e)}")

    @staticmethod
    def save(player: Player) -> None:
        """Save changes to the database for an existing player."""
        try:
            db.execute("""
                UPDATE users 
                SET email = ?, username = ?, password = ?, level = ?, exp = ?, title = ?
                WHERE user_id = ?
            """, (player.email, player.username, player._User__password, 
                 player.level, player.exp, player.title, player.user_id))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving player: {str(e)}")

    @staticmethod
    def gain_exp(player: Player, amount: int) -> None:
        """Increase player's experience and level up if necessary."""
        player.exp += amount
        while player.exp >= player.get_exp_threshold():
            PlayerManager.level_up(player)
        PlayerManager.save(player)

    @staticmethod
    def level_up(player: Player) -> None:
        """Increase player level and adjust experience points."""
        player.level += 1
        player.exp -= player.get_exp_threshold()

        # Update title based on level
        if player.level >= 20:
            player.title = "Legend"
        elif player.level >= 15:
            player.title = "Master"
        elif player.level >= 10:
            player.title = "Expert"
        elif player.level >= 5:
            player.title = "Adept"

        PlayerManager.save(player)
