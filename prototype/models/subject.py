from datetime import datetime

class Subject:
    def __init__(self, id: str, name: str, difficulty: int = 1):
        self.id = id
        self.name = name
        self.difficulty = min(max(difficulty, 1), 5)  # Ensure difficulty is between 1-5
        self.quests = []
        self.notes = []  # Study notes
        self.flashcards = []  # Flashcards
        self.wins = 0
        self.losses = 0
        self.created_at = datetime.now()
        self.last_battle = None

    def add_quest(self, quest) -> None:
        """Add a quest to the subject"""
        self.quests.append(quest)

    def remove_quest(self, quest_id: int) -> bool:
        """Remove a quest from the subject"""
        initial_length = len(self.quests)
        self.quests = [q for q in self.quests if q.id != quest_id]
        return len(self.quests) < initial_length

    def add_note(self, note) -> None:
        """Add a note to the subject"""
        self.notes.append(note)

    def remove_note(self, note_id: int) -> bool:
        """Remove a note from the subject"""
        initial_length = len(self.notes)
        self.notes = [n for n in self.notes if n.id != note_id]
        return len(self.notes) < initial_length

    def add_flashcard(self, flashcard) -> None:
        """Add a flashcard to the subject"""
        self.flashcards.append(flashcard)

    def remove_flashcard(self, flashcard_id: int) -> bool:
        """Remove a flashcard from the subject"""
        initial_length = len(self.flashcards)
        self.flashcards = [f for f in self.flashcards if f.id != flashcard_id]
        return len(self.flashcards) < initial_length    


    def to_dict(self) -> dict:
        """Convert the subject to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'quests': [quest.to_dict() for quest in self.quests],
            'notes': [note.to_dict() for note in self.notes],
            'flashcards': [flashcard.to_dict() for flashcard in self.flashcards],
            'created_at': self.created_at.isoformat(),
            'last_battle': self.last_battle.isoformat() if self.last_battle else None
        }