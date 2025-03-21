from datetime import datetime
from models.content.content_manager import ContentManager

class Content:
    def __init__(self, description: str, subject_id: int, *args, **kwargs):
        self.description = description
        self.subject_id = subject_id
        self.created_at = datetime.now()