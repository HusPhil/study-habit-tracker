from models.content.linkable_content import LinkableContent


class Note(LinkableContent):
    """Represents a Note associated with a Subject."""

    def __init__(self, id: int, description: str, subject_id: int, link):
        super().__init__(link=link, description=description, subject_id=subject_id)  # ✅ Pass `link` to LinkableContent
        self._id = id

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "subject_id": self.subject_id,
            "link": self.link,
        }
    
    @property
    def id(self):
        return self._id