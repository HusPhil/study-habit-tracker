

class Badge:
    
    def __init__(self, title: str, rarity: str):
        self._title = title
        self._rarity = rarity

    def to_string(self):
        return {
            "title": self.title,
            "rarity": self.rarity,
            "file_name": f"{self.title.replace(' ', '_').lower()}.png"
        }

    @property
    def title(self):
        return self._title
    
    @property
    def rarity(self):
        return self._rarity 