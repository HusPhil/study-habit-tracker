from models.content.content import Content

class TrackableContent(Content):
    def __init__(self, description: str, subject_id: int, status: int = 0, difficulty: int = 3):
        
        super().__init__(description, subject_id)
        self.status = status  # int for 0 (not started), 1 (in progress), 2 (completed)
        self.difficulty = difficulty  # string representing difficulty level

