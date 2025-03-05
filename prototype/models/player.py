from models.user import User

class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str, level: int = 1, exp: int = 0):
        super().__init__(user_id, email, username, password)  # Call User constructor
        self.level = level  # Additional attribute for Player
        self.exp = exp  # Experience points
    


















"""
magtry ka kung pano natin ma iimplement yung flash cards at notes

dun sa flashcards, feel ko mahirap hanapan ng Public APIs pero try ka pa din

sa notes naman, baka may mahanap ka kung pano maaccess ang
"""