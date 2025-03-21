from models.badge.badge import Badge
from .enemy_type import EnemyType

class Enemy:
    def __init__(self, id: int, name: str, description: str, health: int):
        self._id = id
        self._name = name
        self._description = description
        self._health = health

    def drop_badge(self):
        return Badge("Dragon Slayer", "Legendary")
    
    def to_dict(self):
        """Convert the enemy object to a dictionary."""
        enemy_type = EnemyType.get_by_name(self.name)  # Use helper function
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "health": self.health,
            "file_name": enemy_type.file_name if enemy_type else None  # Handle missing cases safely
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
    

