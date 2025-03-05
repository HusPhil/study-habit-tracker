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

    def get_active_quests(self) -> list:
        """Get all uncompleted quests"""
        return [quest for quest in self.quests if not quest.completed]

    def get_completed_quests(self) -> list:
        """Get all completed quests"""
        return [quest for quest in self.quests if quest.completed]

    def record_battle(self, won: bool) -> None:
        """Record the result of a battle"""
        if won:
            self.wins += 1
        else:
            self.losses += 1
        self.last_battle = datetime.now()

    def get_win_rate(self) -> float:
        """Calculate the win rate percentage"""
        total_battles = self.wins + self.losses
        return (self.wins / total_battles * 100) if total_battles > 0 else 0

    def get_total_exp_earned(self) -> int:
        """Calculate total experience earned from completed quests"""
        return sum(quest.exp_reward for quest in self.get_completed_quests())

    def to_dict(self) -> dict:
        """Convert the subject to a dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': self.get_win_rate(),
            'total_exp_earned': self.get_total_exp_earned(),
            'quests': [quest.to_dict() for quest in self.quests],
            'notes': [note.to_dict() for note in self.notes],
            'flashcards': [flashcard.to_dict() for flashcard in self.flashcards],
            'created_at': self.created_at.isoformat(),
            'last_battle': self.last_battle.isoformat() if self.last_battle else None
        }