from enum import Enum, auto

class Title(Enum):
    NOOBIE = "Noobie"
    ADEPT = "Adept"
    EXPERT = "Expert"
    MASTER = "Master"
    LEGEND = "Legend"

    @staticmethod
    def get_title(level: int) -> str:
        """Return the title based on the player's level."""
        if level >= 20:
            return Title.LEGEND.value
        elif level >= 15:
            return Title.MASTER.value
        elif level >= 10:
            return Title.EXPERT.value
        elif level >= 5:
            return Title.ADEPT.value
        return Title.NOOBIE.value