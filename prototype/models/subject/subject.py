from datetime import datetime
import random
from typing import List
from models.database.db import db, DatabaseError
from models.quest.quest import Quest
from models.flashcard.flashcard import Flashcard
from models.note.note import Note
from models.enemy.enemy import Enemy, EnemyType


class Subject:
    def __init__(self, id: str, code_name: str, difficulty: int = 1, user_id: int = None):
        self.id = id
        self.user_id = user_id
        self.code_name = code_name
        self.difficulty = min(max(difficulty, 1), 5)  

        self._quests = None  
        self._notes = None
        self._flashcards = None

    def spawnEnemy(self, quests: list) -> List[Enemy]:
        all_enemy_types = list(EnemyType)
    
        random_enemies = random.choices(all_enemy_types, k=len(quests))
        chosen_enemies = []

        print(quests)

        for i, enemy in enumerate(random_enemies):
            newEnemy = Enemy(id=quests[i]['id'], name=enemy.value.monster_name, health=quests[i]['difficulty'], description=quests[i]['description'])
            chosen_enemies.append(newEnemy)
        # print(chosen_enemies)
        return chosen_enemies


    @staticmethod
    def create(code_name: str, description: str, difficulty: int, user_id: int) -> 'Subject':
        """Create a new subject in database"""
        try:
            existing_subject = db.execute("SELECT * FROM subjects WHERE code_name = ? AND user_id = ?", (code_name, user_id))
            if existing_subject:
                data = existing_subject[0]
                return Subject(id=data['subject_id'], code_name=data['code_name'], difficulty=data['difficulty'], user_id=data['user_id'])

            db.execute("INSERT INTO subjects (code_name, description, difficulty, user_id) VALUES (?, ?, ?, ?)",
                       (code_name, description, difficulty, user_id))

            result = db.execute("SELECT * FROM subjects WHERE code_name = ?", (code_name,))
            if result:
                data = result[0]
                return Subject(id=data['subject_id'], code_name=data['code_name'], difficulty=data['difficulty'], user_id=data['user_id'])

            raise DatabaseError("Failed to create subject")
        except DatabaseError as e:
            raise DatabaseError(f"Error creating subject: {str(e)}")

    @staticmethod
    def get(subject_id: int) -> 'Subject':
        """Get a subject by ID"""
        try:
            result = db.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
            if result:
                data = result[0]
                return Subject(id=data['subject_id'], code_name=data['code_name'], difficulty=data['difficulty'], user_id=data['user_id'])
            raise DatabaseError("Subject not found")
        except DatabaseError as e:
            raise DatabaseError(f"Error getting subject: {str(e)}")

    @staticmethod
    def get_all(user_id: int) -> list:
        """Get all subjects for a user"""
        try:
            results = db.execute("SELECT * FROM subjects WHERE user_id = ?", (user_id,))
            subjects = []
            for result in results:
                subjects.append(Subject(
                    id=result['subject_id'],
                    code_name=result['code_name'],
                    difficulty=result['difficulty'],
                    user_id=result['user_id']
                ))
            return subjects
        except DatabaseError as e:
            raise DatabaseError(f"Error getting subjects: {str(e)}")

    @property
    def quests(self):
        """Lazy load quests only when accessed"""
        if self._quests is None:
            self._quests = self.get_quests()
        return self._quests

    @property
    def notes(self):
        """Lazy load notes only when accessed"""
        if self._notes is None:
            self._notes = []
        return self._notes

    @property
    def flashcards(self):
        """Lazy load flashcards only when accessed"""
        if self._flashcards is None:
            self._flashcards = self.get_flashcards()
        return self._flashcards
    
    def get_quests(self) -> list:
        """Retrieve all quests for this subject dynamically"""
        try:
            results = db.execute("SELECT * FROM quests WHERE subject_id = ?", (self.id,))
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

    def add_quest(self, quest: Quest) -> None:
        """Add a quest to the subject"""
        db.execute("INSERT INTO quests (description, subject_id, status, difficulty) VALUES (?, ?, ?, ?)",
                   (quest.description, self.id, quest.status, quest.difficulty))
    def get_flashcards(self) -> list:
        """Retrieve all flashcards for this subject dynamically."""
        try:
            results = db.execute("SELECT * FROM flashcards WHERE subject_id = ?", (self.id,))  # ✅ Fetch flashcards
            

            flashcards = []
            for result in results:
                flashcards.append(Flashcard(
                    id=result['flashcard_id'],
                    description=result['description'],
                    link=result['link'],
                    subject_id=result['subject_id'],
                    status=result['status'],    
                ))
            print("Flashcard query results:", flashcards)
            return flashcards  # ✅ Returns a list of Flashcard objects
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving flashcards: {str(e)}")
        
    def get_notes(self) -> list:
        """Retrieve all flashcards for this subject dynamically."""
        try:
            results = db.execute("SELECT * FROM notes WHERE subject_id = ?", (self.id,))  # ✅ Fetch flashcards
            

            notes = []
            for result in results:
                notes.append(Note(
                    id=result['note_id'],
                    subject_id=result['subject_id'],
                    description=result['description'],
                    link=result['link'],
                ))
            print("Flashcard query results:", notes)
            return notes  # ✅ Returns a list of Flashcard objects
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving flashcards: {str(e)}")


    def to_dict(self) -> dict:
        """Convert the subject to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'code_name': self.code_name,
            'difficulty': self.difficulty,
            'quests': [quest.to_dict() for quest in self.get_quests()],  # ✅ Lazy load
            'notes': [note.to_dict() for note in self.notes],  # ✅ Lazy load
            'flashcards': [flashcard.to_dict() for flashcard in self.flashcards],  # ✅ Lazy load
            'user_id': self.user_id
        }
