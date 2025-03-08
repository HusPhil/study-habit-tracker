# models/player.py
from .user import User
from datetime import datetime
from .db import db, DatabaseError
from .subject import Subject
from werkzeug.security import generate_password_hash

class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str, 
                 level: int = 1, exp: int = 0, title: str = "Noobie"):
        super().__init__(user_id, email, username, password)
        self.title = title
        self.level = level
        self.exp = exp
        self.items = []
        self.subjects = []

    @staticmethod
    def create(email: str, username: str, password: str) -> 'Player':
        """Create a new player in database"""
        try:
            existing_player = db.execute("SELECT * FROM users WHERE email = ?", (email,))
            if existing_player:
                # If it exists, return the existing player
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
            # Insert the user data
            hashed_password = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (email, username, password, level, exp, title) VALUES (?, ?, ?, ?, ?, ?)",
                (email, username, hashed_password, 1, 0, "Noobie")
            )
            
            # Get the created player
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
    def get(user_id: int) -> 'Player':
        """Get player from database"""
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

    def save(self) -> None:
        """Save changes to database"""
        try:
            db.execute("""
                UPDATE users 
                SET email = ?, username = ?, password = ?, level = ?, exp = ?, title = ?
                WHERE user_id = ?
            """, (self.email, self.username, self._User__password, 
                 self.level, self.exp, self.title, self.user_id))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving player: {str(e)}")

    def get_exp_threshold(self) -> int:
        """Get experience points needed for next level"""
        return self.level * 100

    def gain_exp(self, amount: int) -> None:
        """Gain experience points and level up if threshold reached"""
        self.exp += amount
        while self.exp >= self.get_exp_threshold():
            self.level_up()
        self.save()
            
    def level_up(self) -> None:
        """Level up the player and adjust exp points"""
        self.level += 1
        self.exp -= self.get_exp_threshold()
        
        # Update title based on level
        if self.level >= 20:
            self.title = "Legend"
        elif self.level >= 15:
            self.title = "Master"
        elif self.level >= 10:
            self.title = "Expert"
        elif self.level >= 5:
            self.title = "Adept"
        
        self.save()

    def to_dict(self) -> dict:
        """Return dictionary representation of player"""
        base_dict = super().to_dict()
        base_dict.update({
            'level': self.level,
            'exp': self.exp,
            'title': self.title,
            'exp_threshold': self.get_exp_threshold()
        })
        return base_dict