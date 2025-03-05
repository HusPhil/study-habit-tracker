from models.content import Content

class TrackableContent(Content):
    def __init__(self, description: str, subject=None, status: bool = False, difficulty: str = "easy"):
        super().__init__(description, subject)
        self.status = status  # boolean to track completion
        self.difficulty = difficulty  # string representing difficulty level
