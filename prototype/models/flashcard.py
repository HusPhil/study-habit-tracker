from models.trackable_content import TrackableContent
from models.db import db

class Flashcard(TrackableContent):
    def __init__(self, id=None, question="", answer="", subject_id=None, status=False, difficulty="Easy"):
        super().__init__(status, difficulty)
        self.id = id
        self.question = question
        self.answer = answer
        self.subject_id = subject_id  # Foreign key linking to a Subject

    @staticmethod
    def create(question: str, answer: str, subject_id: int, difficulty: str = "Easy") -> 'Flashcard':
        """Create a new flashcard and store it in the database"""
        query = """
        INSERT INTO flashcards (question, answer, subject_id, status, difficulty) 
        VALUES (?, ?, ?, ?, ?) RETURNING id
        """
        result = db.execute(query, (question, answer, subject_id, False, difficulty))
        db.commit()
        flashcard_id = result[0]['id'] if result else None
        return Flashcard(id=flashcard_id, question=question, answer=answer, subject_id=subject_id, status=False, difficulty=difficulty)

    @staticmethod
    def get_all():
        """Retrieve all flashcards"""
        query = "SELECT * FROM flashcards"
        return [Flashcard(**data) for data in db.fetch_all(query)]

    @staticmethod
    def get_by_id(flashcard_id):
        """Retrieve a single flashcard by ID"""
        query = "SELECT * FROM flashcards WHERE id = ?"
        data = db.fetch_one(query, (flashcard_id,))
        return Flashcard(**data) if data else None

    def update(self, question=None, answer=None, status=None, difficulty=None):
        """Update flashcard details"""
        query = "UPDATE flashcards SET question = ?, answer = ?, status = ?, difficulty = ? WHERE id = ?"
        db.execute(query, (question or self.question, answer or self.answer, status or self.status, difficulty or self.difficulty, self.id))
        db.commit()

    @staticmethod
    def delete(flashcard_id):
        """Delete a flashcard by ID"""
        query = "DELETE FROM flashcards WHERE id = ?"
        db.execute(query, (flashcard_id,))
        db.commit()
