from models.content.linkable_content import LinkableContent


class Note(LinkableContent):
    """Represents a Note associated with a Subject."""

    def __init__(self, id: int = None, description: str = "", subject_id: int = None, link: str = ""):
        super().__init__(link=link, description=description, subject_id=subject_id)  # ✅ Pass `link` to LinkableContent
        self.id = id
