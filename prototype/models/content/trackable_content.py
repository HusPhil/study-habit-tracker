from models.content.content import Content

class TrackableContent(Content):
    def __init__(self, description: str, subject_id: int, status: int = 0, *args, **kwargs):
        super().__init__(description, subject_id, *args, **kwargs)  # Pass extra args for multiple inheritance
        self._status = status


    @property
    def status(self):
        return self._status