from models.database.db import db, DatabaseError
from models.quest.quest import Quest
from models.flashcard.flashcard import Flashcard
from models.note.note import Note
from models.quest.quest_manager import QuestManager
from models.flashcard.flashcard_manager import FlashcardManager
from models.note.note_manager import NoteManager

class SubjectManager:
    """Handles all database operations for subjects without directly importing Subject."""

    @staticmethod
    def create(code_name: str, description: str, difficulty: int, user_id: int):
        """Creates a new subject in the database and returns its ID."""
        try:
            existing_subject = db.execute(
                "SELECT * FROM subjects WHERE code_name = ? AND user_id = ?", 
                (code_name, user_id)
            )
            if existing_subject:
                return existing_subject[0]['subject_id']  # ✅ Return existing subject ID

            db.execute(
                "INSERT INTO subjects (code_name, description, difficulty, user_id) VALUES (?, ?, ?, ?)",
                (code_name, description, difficulty, user_id)
            )

            result = db.execute("SELECT subject_id FROM subjects WHERE code_name = ?", (code_name,))
            return result[0]['subject_id'] if result else None  # ✅ Return new subject ID
        except DatabaseError as e:
            raise DatabaseError(f"Error creating subject: {str(e)}")

    @staticmethod
    def get(subject_id: int):
        """Fetches subject details by ID."""
        try:
            result = db.execute("SELECT * FROM subjects WHERE subject_id = ?", (subject_id,))
            return result[0] if result else None  # ✅ Return subject data (dict)
        except DatabaseError as e:
            raise DatabaseError(f"Error getting subject: {str(e)}")

    @staticmethod
    def get_all(user_id: int):
        """Retrieves all subjects for a user."""
        try:
            return db.execute("SELECT * FROM subjects WHERE user_id = ?", (user_id,))
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving subjects: {str(e)}")
        
    from models.database.db import db, DatabaseError

    @staticmethod
    def get_all_with_details(user_id: int) -> list:
        """Retrieves all subjects for a user along with their quests, notes, and flashcards."""
        try:
            # Fetch all subjects for the user
            subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", (user_id,))
            if not subjects:
                return []

            subject_list = []
            for subject in subjects:
                subject_id = subject["subject_id"]

                # Fetch related quests
                quests = db.execute("SELECT * FROM quests WHERE subject_id = ?", (subject_id,))
                # Fetch related flashcards
                flashcards = db.execute("SELECT * FROM flashcards WHERE subject_id = ?", (subject_id,))
                # Fetch related notes
                notes = db.execute("SELECT * FROM notes WHERE subject_id = ?", (subject_id,))

                # Construct subject dictionary
                subject_data = {
                    "id": subject_id,
                    "code_name": subject["code_name"],
                    "difficulty": subject["difficulty"],
                    "user_id": subject["user_id"],
                    "quests": [dict(q) for q in quests],
                    "flashcards": [dict(f) for f in flashcards],
                    "notes": [dict(n) for n in notes]
                }

                subject_list.append(subject_data)

            return subject_list

        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving subjects: {str(e)}")

    @staticmethod
    def get_quests(subject_id: int):
        """Retrieves all quests for a subject."""
        try:
            results = db.execute("SELECT * FROM quests WHERE subject_id = ?", (subject_id,))
            quests = []

            for r in results:
                q = Quest(id=r['quest_id'], description=r['description'], status=r['status'], difficulty=r['difficulty'])
                quests.append(q)

            return quests  # ✅ Return a list of Quest objects
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving quests: {str(e)}")

    @staticmethod
    def add_quest(subject_id: int, quest: Quest):
        """Adds a quest to the database for the given subject."""
        try:
            db.execute(
                "INSERT INTO quests (description, subject_id, status, difficulty) VALUES (?, ?, ?, ?)",
                (quest.description, subject_id, quest.status, quest.difficulty)
            )
        except DatabaseError as e:
            raise DatabaseError(f"Error adding quest: {str(e)}")

    @staticmethod
    def get_flashcards(subject_id: int):
        """Retrieves all flashcards for a subject."""
        try:
            results = db.execute("SELECT * FROM flashcards WHERE subject_id = ?", (subject_id,))
            return [Flashcard(id=r['flashcard_id'], description=r['description'], subject_id=r['subject_id'], 
                              link=r['link'], status=r['status']) for r in results]
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving flashcards: {str(e)}")

    @staticmethod
    def get_notes(subject_id: int):
        """Retrieves all notes for a subject."""
        try:
            results = db.execute("SELECT * FROM notes WHERE subject_id = ?", (subject_id,))
            notes = []

            for r in results:
                note = Note(id=r['note_id'], description=r['description'], subject_id=r['subject_id'], link=r['link'])
                print("notes", note)
                notes.append(note)
            return notes
        except DatabaseError as e:
            raise DatabaseError(f"Error retrieving notes: {str(e)}")
