from models.quest.quest import Quest
from models.flashcard.flashcard import Flashcard
from models.note.note import Note
from models.enemy.enemy import Enemy, EnemyType
from models.subject.subject_manager import SubjectManager  # ✅ Use SubjectManager
import random

class Subject:
    def __init__(self, id: str, code_name: str, difficulty: int = 1, user_id: int = None):
        self._id = id
        self._user_id = user_id
        self._code_name = code_name
        self._difficulty = min(max(difficulty, 1), 5)  

    def spawnEnemy(self, quests: list):
        """Creates a list of enemies based on quests' difficulties."""
        all_enemy_types = list(EnemyType)
        chosen_enemies = []

        for i, enemy_type in enumerate(random.choices(all_enemy_types, k=len(quests))):
            chosen_enemies.append(Enemy(
                id=quests[i]['id'], 
                name=enemy_type.value.monster_name, 
                health=quests[i]['difficulty'], 
                description=quests[i]['description']
            ))
        return chosen_enemies

    def to_dict(self):
        """Convert the subject to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'code_name': self.code_name,
            'difficulty': self.difficulty,
            'user_id': self.user_id
        }
    
    @property
    def id(self):
        return self._id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def code_name(self):
        return self._code_name
    
    @property
    def difficulty(self):
        return self._difficulty
