from models.user.user import User

class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str, 
                 level: int = 1, exp: int = 0, title: str = "Noobie"):
        super().__init__(user_id, email, username, password)
        self.title = title
        self.level = level
        self.exp = exp
        self.badges = []

    def get_exp_threshold(self) -> int:
        """Get experience points needed for the next level."""
        return self.level * 100

    def to_dict(self) -> dict:
        """Return a dictionary representation of the player."""
        base_dict = super().to_dict()
        base_dict.update({
            'level': self.level,
            'exp': self.exp,
            'title': self.title,
            'exp_threshold': self.get_exp_threshold()
        })
        return base_dict
