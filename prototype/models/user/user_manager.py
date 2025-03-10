from models.database.db import db, DatabaseError
from models.user import User
from typing import Optional
from werkzeug.security import generate_password_hash

class UserManager:
    @staticmethod
    def create(email: str, username: str, password: str) -> User:
        """Create a new user in the database."""
        try:
            hashed_password = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                (email, username, hashed_password)
            )
            # Retrieve the newly created user
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
    def get(user_id: int) -> Optional[User]:
        """Retrieve a user from the database."""
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

    @staticmethod
    def save(user: User) -> None:
        """Save changes to the database for an existing user."""
        try:
            db.execute("""
                UPDATE users 
                SET email = ?, username = ?, password = ?
                WHERE user_id = ?
            """, (user.email, user.username, user._User__password, user.user_id))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving user: {str(e)}")
