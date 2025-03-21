from datetime import datetime
import random
from typing import List
from models.database.db import db, DatabaseError
from models.quest.quest import Quest
from models.enemy.enemy import Enemy, EnemyType

class Subject:
    def __init__(self, subjectId: str, description: str):
        self.subjectId = subjectId
        self.description = description
        self._quests = None  
        self._notes = []
        self._flashcards = []

    def spawnEnemy(self, quests: list) -> List[Enemy]:
        all_enemy_types = list(EnemyType)
    
        random_enemies = random.choices(all_enemy_types, k=len(quests))
        chosen_enemies = []

        for i, enemy in enumerate(random_enemies):
            newEnemy = Enemy(id=quests[i]['id'], name=enemy.value.monster_name, health=quests[i]['difficulty'], description=quests[i]['description'])
            chosen_enemies.append(newEnemy)
        return chosen_enemies

    def getQuests(self) -> list:
        if self._quests is None:
            self._quests = SubjectManager.get_quests(self.subjectId)
        return self._quests

class SubjectManager:
    @staticmethod
    def create(code_name: str, description: str, difficulty: int, user_id: int) -> Subject:
        try:
            existing_subject = db.execute("SELECT * FROM subjects WHERE code_name = ? AND user_id = ?", (code_name, user_id))
            if existing_subject:
                data = existing_subject[0]
                return Subject(subjectId=data['subject_id'], description=data['description'])

            db.execute("INSERT INTO subjects (code_name, description, difficulty, user_id) VALUES (?, ?, ?, ?)",
                       (code_name, description, difficulty, user_id))

            result = db.execute("SELECT * FROM subjects WHERE code_name = ?", (code_name,))
            if result:
                data = result[0]
                return Subject(subjectId=data['subject_id'], description=data['description'])

            raise DatabaseError("Failed to create subject")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating subject: {str(e)}")

    @staticmethod
    def get(subject_id: int) -> Subject:
        try:
            result = db.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
            if result:
                data = result[0]
                return Subject(subjectId=data['subject_id'], description=data['description'])
            raise DatabaseError("Subject not found")
        except DatabaseError as e:
            raise DatabaseError(f"Error getting subject: {str(e)}")

    @staticmethod
    def get_quests(subject_id: int) -> list:
        try:
            results = db.execute("SELECT * FROM quests WHERE subject_id = ?", (subject_id,))
            quests = []
            for result in results:
                quests.append(Quest(
                    id=result['quest_id'],
                    description=result['description'],
                    status=result['status'],
                    difficulty=result['difficulty']
                ))
            return quests
        except DatabaseError as e:
            raise DatabaseError(f"Error getting quests: {str(e)}")
