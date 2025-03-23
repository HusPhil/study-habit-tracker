

class Badge:
    
    def __init__(self, title: str, rarity: str, description: str):
        self._title = title
        self._rarity = rarity
        self._description = description

    def to_string(self):
        return {
            "title": self.title,
            "rarity": self.rarity,
            "description": self.description,
            "file_name": f"{self.title.replace(' ', '_').lower()}.png"
        }

    @property
    def title(self):
        return self._title
    
    @property
    def rarity(self):
        return self._rarity 

    @property
    def description(self):
        return self._description    
