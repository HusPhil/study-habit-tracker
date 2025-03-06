from datetime import datetime
from .db import db
from .quest import Quest

class Subject:
    def __init__(self, id: str, name: str, difficulty: int = 1, user_id: int = None):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.difficulty = min(max(difficulty, 1), 5)  # Ensure difficulty is between 1-5
        self.quests = []
        self.notes = []  # Study notes
        self.flashcards = [] 

    def add_quest(self, quest) -> None:
        """Add a quest to the subject"""
        try:
            with db.transaction() as conn:
                self.quests.append(quest)
                quest.subject_id = self.id
                quest.save()
        except Exception as e:
            conn.rollback()
            raise e

    def remove_quest(self, quest_id: int) -> bool:
        """Remove a quest from the subject"""
        try:
            with db.transaction() as conn:
                c = conn.cursor()
                initial_length = len(self.quests)
                c.execute("DELETE FROM quests WHERE id = ?", (quest_id,))
                self.quests = [q for q in self.quests if q.id != quest_id]
                return len(self.quests) < initial_length
        except Exception as e:
            conn.rollback()
            raise e

    def add_note(self, note) -> None:
        """Add a note to the subject"""
        try:
            with db.transaction() as conn:
                self.notes.append(note)
                note.subject_id = self.id
                note.save()
        except Exception as e:
            conn.rollback()
            raise e

    def remove_note(self, note_id: int) -> bool:
        """Remove a note from the subject"""
        try:
            with db.transaction() as conn:
                c = conn.cursor()
                initial_length = len(self.notes)
                c.execute("DELETE FROM notes WHERE id = ?", (note_id,))
                self.notes = [n for n in self.notes if n.id != note_id]
                return len(self.notes) < initial_length
        except Exception as e:
            conn.rollback()
            raise e

    def add_flashcard(self, flashcard) -> None:
        """Add a flashcard to the subject"""
        try:
            with db.transaction() as conn:
                self.flashcards.append(flashcard)
                flashcard.subject_id = self.id
                flashcard.save()
        except Exception as e:
            conn.rollback()
            raise e

    def remove_flashcard(self, flashcard_id: int) -> bool:
        """Remove a flashcard from the subject"""
        try:
            with db.transaction() as conn:
                c = conn.cursor()
                initial_length = len(self.flashcards)
                c.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
                self.flashcards = [f for f in self.flashcards if f.id != flashcard_id]
                return len(self.flashcards) < initial_length
        except Exception as e:
            conn.rollback()
            raise e

    def to_dict(self) -> dict:
        """Convert the subject to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'quests': [quest.to_dict() for quest in self.quests],
            'notes': [note.to_dict() for note in self.notes],
            'flashcards': [flashcard.to_dict() for flashcard in self.flashcards],
            'wins': self.wins,
            'losses': self.losses,
            'created_at': self.created_at.isoformat(),
            'last_battle': self.last_battle.isoformat() if self.last_battle else None,
            'user_id': self.user_id
        }