from models.database.db import db, DatabaseError
from typing import Optional
from werkzeug.security import generate_password_hash

class UserManager:
    @staticmethod
    def create(email: str, username: str, password: str) -> dict:
        """Create a new user in the database and return user data as a dictionary."""
        try:
            hashed_password = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
                (email, username, hashed_password)
            )

            # Retrieve the newly created user
            result = db.execute("SELECT user_id, email, username FROM users WHERE email = ?", (email,))
            if result:
                return dict(result[0])  # ✅ Return as dictionary instead of User object
            
            raise DatabaseError("Failed to create user")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating user: {str(e)}")

    @staticmethod
    def get(user_id: int) -> Optional[dict]:
        """Retrieve a user from the database and return as a dictionary."""
        try:
            result = db.execute("SELECT user_id, email, username FROM users WHERE user_id = ?", (user_id,))
            if result:
                retrieved_data = dict(result[0])
                retrieved_data['password'] = '<hidden>'
                return retrieved_data  # ✅ Return dictionary
            
            return None
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving user: {str(e)}")

    @staticmethod
    def save(user_data: dict) -> None:
        """Save changes to the database for an existing user using dictionary data."""
        try:
            db.execute("""
                UPDATE users 
                SET email = ?, username = ?, password = ?
                WHERE user_id = ?
            """, (user_data["email"], user_data["username"], user_data["password"], user_data["user_id"]))
        except DatabaseError as e:
            raise DatabaseError(f"Error saving user: {str(e)}")
