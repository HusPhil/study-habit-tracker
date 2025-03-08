from models.trackable_content import TrackableContent
from models.db import db

class Flashcard(TrackableContent):
    def __init__(self, question, answer, subject_id, status=False, difficulty="Easy"):
        super().__init__(status, difficulty)
        self.question = question
        self.answer = answer
        self.subject_id = subject_id  # Foreign key linking to a subject

    def save_to_db(self):
        """Save flashcard data to the database"""
        query = """
        INSERT INTO flashcards (question, answer, subject_id, status, difficulty) 
        VALUES (?, ?, ?, ?, ?)
        """
        db.execute(query, (self.question, self.answer, self.subject_id, self.status, self.difficulty))
        db.commit()

    @staticmethod
    def get_all():
        """Retrieve all flashcards"""
        query = "SELECT * FROM flashcards"
        return db.fetch_all(query)

    @staticmethod
    def get_by_id(flashcard_id):
        """Retrieve a single flashcard by ID"""
        query = "SELECT * FROM flashcards WHERE id = ?"
        return db.fetch_one(query, (flashcard_id,))

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
