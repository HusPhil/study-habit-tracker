from models.trackable_content import TrackableContent
from models.linkable_content import LinkableContent
from models.db import db

class Note(TrackableContent, LinkableContent):
    def __init__(self, id: int = None, content: str = "", subject_id: int = None, link: str = "", status: bool = False, difficulty: str = "Easy"):
        super().__init__(status=status, difficulty=difficulty)
        self.id = id
        self.content = content
        self.subject_id = subject_id
        self.link = link  

    @staticmethod
    def create(content: str, subject_id: int, link: str = "", status: bool = False, difficulty: str = "Easy") -> 'Note':
        """Create a new Note in the database"""
        try:
            query = """
            INSERT INTO notes (content, subject_id, link, status, difficulty) 
            VALUES (?, ?, ?, ?, ?) RETURNING id
            """
            result = db.execute(query, (content, subject_id, link, status, difficulty))
            db.commit()

            note_id = result[0]['id'] if result else None
            return Note(id=note_id, content=content, subject_id=subject_id, link=link, status=status, difficulty=difficulty)

        except Exception as e:
            db.rollback()
            raise Exception(f"Error creating note: {str(e)}")

    def to_dict(self) -> dict:
        """Convert Note object to dictionary format"""
        return {
            'id': self.id,
            'content': self.content,
            'subject_id': self.subject_id,
            'link': self.link,
            'status': self.status,  
            'difficulty': self.difficulty  
        }
