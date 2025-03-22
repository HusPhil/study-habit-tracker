from werkzeug.security import check_password_hash
from flask import session


class User:
    def __init__(self, user_id: int, email: str, username: str, password: str):
        self._id = user_id  # Encapsulated but accessible via `.id`
        self.username = username
        self.email = email      
        self.__password = password  # Keep password private
    
    def login(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        if check_password_hash(self.__password, password):
            session['user_id'] = self.id  # ✅ Uses the property
            return True
        return False

    def logout(self) -> None:
        """Log the user out."""
        session.clear()


    def to_dict(self) -> dict:
        """Return a dictionary representation of the user."""
        return {
            'user_id': self.id,  # ✅ Uses the property
            'email': self.email,
            'username': self.username
        }

    @property
    def id(self):
        return self._id

