# models/user.py
from .db import db, DatabaseError
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, user_id: int, email: str, username: str, password: str):
        self.user_id = user_id          
        self.email = email      
        self.username = username
        self.__password = password

    @staticmethod
    def create(email: str, username: str, password: str) -> 'User':
        """Create a new user in database"""
        try:
            hashed_password = generate_password_hash(password)
            print(hashed_password)
            db.execute(
                "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                (email, username, hashed_password)
            )
            # Get the created user
            result = db.execute("SELECT * FROM users WHERE email = ?", (email,))
            if result:
                data = result[0]
                return User(
                    user_id=data['user_id'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password']
                )
            raise DatabaseError("Failed to create user")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating user: {str(e)}")

    @staticmethod
    def get(user_id: int) -> Optional['User']:
        """Get user from database"""
        try:
            result = db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            if result:
                data = result[0]
                return User(
                    user_id=data['user_id'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password']
                )
            return None
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving user: {str(e)}")

    def save(self) -> None:
        """Save changes to database"""
        try:
            db.execute("""
                UPDATE users 
                SET email = ?, username = ?, password = ?
                WHERE user_id = ?
            """, (self.email, self.username, self.__password, self.user_id))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving user: {str(e)}")

    def to_dict(self):
        """Return dictionary representation of user"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username
        }

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches"""
        return check_password_hash(self.__password, password)