from models.content.trackable_content import TrackableContent
from models.content.linkable_content import LinkableContent
from models.flashcard.flashcard_manager import FlashcardManager

class Flashcard(TrackableContent, LinkableContent):
    """Represents a flashcard with tracking capabilities."""
    
    def __init__(self, id: int, description: str, subject_id: int, link: str, status: bool = False, difficulty: int = 3):
            # Initialize both parent classes properly
            TrackableContent.__init__(self, id, description, subject_id, status, difficulty)
            LinkableContent.__init__(self, id, description, subject_id, link)

            self.id = id