from datetime import datetime
from models.content.content_manager import ContentManager

class Content:
    def __init__(self, description: str, subject_id: int, *args, **kwargs):
        self._description = description
        self._subject_id = subject_id
        self._created_at = datetime.now()


    @property
    def description(self):
        return self._description
    
    @property
    def subject_id(self):
        return self._subject_id
    
    @property
    def created_at(self):
        return self._created_at