from models.content.trackable_content import TrackableContent
from models.content.linkable_content import LinkableContent
from models.flashcard.flashcard_manager import FlashcardManager

class Flashcard(TrackableContent, LinkableContent):
    """Represents a flashcard with tracking and linking capabilities."""
    
    def __init__(self, id: int, description: str, subject_id: int, link: str, status: int = 0):

        super().__init__(description=description, subject_id=subject_id, status=status, link=link)
        self._id = id 


    def to_dict(self):
        """Converts the flashcard object to a dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "subject_id": self.subject_id,
            "link": self.link,
            "status": self.status,
        }

    @property
    def id(self):
        return self._id