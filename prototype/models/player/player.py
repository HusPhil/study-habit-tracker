from models.user.user import User
from .title import Title
from .player_manager import PlayerManager


class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str,
                 level: int = 1, exp: int = 0, title: str = Title.NOOBIE.value):
        super().__init__(user_id, email, username, password)
        self._level = max(1, level)  # Ensures level is at least 1
        self._exp = max(0, exp)  # Ensures exp is never negative
        self._title = title
        self._badges = []

    def gain_exp(self, amount: int) -> None:
        """Gain experience and level up if necessary."""
        
        self.exp += amount
        
        while self.exp >= PlayerManager.get_exp_threshold(self.level):
            self.level_up()

    def level_up(self) -> None:
        """Increase player level and reset exp after leveling up."""
        self.level += 1
        self.exp = 0  # Reset exp after level-up
        
    def _update_title(self) -> None:
        """Update title based on level."""
        title_map = {
            20: Title.LEGEND.value,
            15: Title.MASTER.value,
            10: Title.EXPERT.value,
            5: Title.ADEPT.value
        }
        self._title = next((title for lvl, title in title_map.items() if self.level >= lvl), Title.NOOBIE.value)

    def to_dict(self) -> dict:
        """Convert player to dictionary."""
        return {
            'user_id': self.id,
            'email': self.email,
            'username': self.username,
            'level': self.level,
            'exp': self.exp,
            'title': self.title
        }

    @property
    def level(self):
        
        return self._level

    @level.setter
    def level(self, new_level: int):
        if new_level < 1:
            raise ValueError("Level cannot be less than 1.")
        self._level = new_level
        self._update_title()

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, amount: int):
        if amount < 0:
            self._exp = 0  # Prevents negative exp
        else:
            self._exp = amount

    @property
    def title(self):
        return self._title
    
    @property
    def badges(self):    
        return self._badges