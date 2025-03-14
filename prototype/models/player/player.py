from models.user.user import User
from .title import Title
from .player_manager import PlayerManager


class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str,
                 level: int = 1, exp: int = 0, title: str = Title.NOOBIE.value):
        super().__init__(user_id, email, username, password)
        self.level = level
        self.exp = exp
        self.title = title

    def gain_exp(self, amount: int) -> None:
        """Gain experience and level up if necessary."""
        self.exp += amount
        while self.exp >= PlayerManager.get_exp_threshold(self.level):
            self.level_up()

    def level_up(self):
        """Increase player level and update title based on level."""
        self.level += 1
        self.exp = 0  # Reset excess exp

        # Update title based on level
        title_map = {
            20: Title.LEGEND.value,
            15: Title.MASTER.value,
            10: Title.EXPERT.value,
            5: Title.ADEPT.value
        }
        self.title = next((title for lvl, title in title_map.items() if self.level >= lvl), Title.NOOBIE.value)
        

    def to_dict(self):
        """Convert player to dictionary."""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'username': self.username,
            'level': self.level,
            'exp': self.exp,
            'title': self.title
        }