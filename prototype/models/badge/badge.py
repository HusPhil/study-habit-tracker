class Badge:
    
    def __init__(self, title: str, rarity):
        self._title = title
        self._rarity = rarity


    @property
    def title(self):
        return self._title
    
    @property
    def rarity(self):
        return self._rarity 