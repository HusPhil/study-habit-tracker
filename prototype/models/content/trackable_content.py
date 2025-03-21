from models.content.content import Content

class TrackableContent(Content):
    def __init__(self, description: str, subject_id: int, status: bool = False, difficulty: str = "easy"):
        super().__init__(description, subject_id)
        self.status = status  # boolean to track completion
        self.difficulty = difficulty  # string representing difficulty level

