from datetime import datetime

class Content:
    def __init__(self, description: str, subject=None):
        self.description = description
        self.subject = subject
        self.created_at = datetime.now()

    def create(self):
        """Create a new content instance"""
        pass