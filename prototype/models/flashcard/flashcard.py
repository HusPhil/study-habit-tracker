from models.content.trackable_content import TrackableContent
from models.subject.subject import Subject

class Flashcard(TrackableContent):
    """Represents a flashcard with tracking capabilities."""

    def __init__(self, id: int, description: str, subject_id: int,  status: bool = False, difficulty: int = 1):
        
        super().__init__(
            status=status, difficulty=difficulty, 
            description=description, subject_id=subject_id
        )

        self.id = id
