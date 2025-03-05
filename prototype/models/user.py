class User:
    def __init__(self, user_id: int, email: str, username: str, password: str):
        self.user_id = user_id          
        self.email = email      
        self.username = username
        self.__password = password

    def login(self) -> bool:
        """Simulates user login (returns True for successful login)."""
        print(self.username, "has just logged in!")
        return True  # Placeholder for authentication logic

    def logout(self) -> None:
        """Logs the user out."""
        print("User logged out.")

    def __hashPassword(self) -> str:
        """Hashes the password (simulated for now)."""
        print("CALLED HASHING FOR:", self.__password)
        return "hashed_" + self.__password  # Placeholder for actual hashing

    def _updateProfile(self, name: str, email: str) -> None:
        """Protected method to update username and email."""
        self.username = name
        self.email = email
