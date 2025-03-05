# models/user.py
from .db import db

class User:
    def __init__(self, user_id: int, email: str, username: str, password: str):
        self.user_id = user_id          
        self.email = email      
        self.username = username
        self.__password = password

    @staticmethod
    def create(email: str, username: str, password: str) -> 'User':
        print("CREATING USER")
        
        """Create a new user in database"""
        query = "INSERT INTO users (email, username, password, type) VALUES (?, ?, ?, ?)"
        db.execute(query, (email, username, password, 'user'))
        # Get the created user
        result = db.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        user_id = result[0][0]
        print("USER CREATED!")
        return User(user_id, email, username, password)

    @staticmethod
    def get(user_id: int) -> 'User':
        """Get user from database"""
        result = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if result:
            user_data = result[0]
            return User(user_data[0], user_data[1], user_data[2], user_data[3])
        return None

    def save(self) -> None:
        """Save changes to database"""
        query = """
            UPDATE users 
            SET email = ?, username = ?, password = ?
            WHERE user_id = ?
        """
        db.execute(query, (self.email, self.username, self.__password, self.user_id))

    def login(self) -> bool:
        """Simulates user login (returns True for successful login)."""
        return True