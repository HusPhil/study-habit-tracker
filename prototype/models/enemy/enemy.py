from models.badge.badge import Badge
from .enemy_type import EnemyType
import random
from models.badge.badge import Badge

class Enemy:
    def __init__(self, id: int, name: str, description: str, health: int):
        self._id = id
        self._name = name
        self._description = description
        self._health = health

    @staticmethod
    def drop_badge(sure_drop: dict):

        if sure_drop:
            return Badge(sure_drop["title"], sure_drop["rarity"], sure_drop["description"])

        """Randomly selects a badge upon enemy defeat."""


        badge_pool = [
            Badge("Novice", "Common", "First Steps"),  
            Badge("Apprentice", "Uncommon", "New Learner"),
            Badge("Warrior", "Rare", "Battle Ready"),
            Badge("Champion", "Epic", "Great Victory"),
            Badge("Legend", "Legendary", "Ultimate Honor"),
        ]

        
        # Weighted probability for badges (higher index = rarer)
        probabilities = [0.05, 0.15, 0.25, 0.30, 0.25]  # Adjusted based on rarity
        
        return random.choices(badge_pool, probabilities)[0]

    def to_dict(self):
        """Convert the enemy object to a dictionary."""
        enemy_type = EnemyType.get_by_name(self.name)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "file_name": enemy_type.file_name if enemy_type else None
        }

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def health(self):
        return self._health



    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def health(self):
        return self._health
    

