from models.content.content import Content
from models.database.db import db, DatabaseError
import re


class LinkableContent(Content):
    """Represents content that contains a link (e.g., Flashcards)."""

    def __init__(self, description: str, subject_id: int, link: str, *args, **kwargs):
        super().__init__(description, subject_id, *args, **kwargs)  # Pass extra args for multiple inheritance
        self._link = link


    @staticmethod
    def verify_link(link: str) -> bool:
        """Verify that a link is valid (basic URL validation)."""
        if not link:
            return False  # Reject empty links
        
        # Basic URL pattern validation
        url_pattern = re.compile(
            r"^(https?:\/\/)?"  # Optional scheme (http or https)
            r"([\da-z\.-]+)\.([a-z\.]{2,6})"  # Domain name
            r"([\/\w\.-]*)*\/?$"  # Path
        )
        
        return bool(url_pattern.match(link))
    
    @property
    def link(self):
        return self._link