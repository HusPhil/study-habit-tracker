from models.user import User
from datetime import datetime
import requests

class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str, level: int = 1, exp: int = 0, title: str = "Noobie"):
        super().__init__(user_id, email, username, password)  # Call User constructor
        self.title = title
        self.level = level
        self.exp = exp
        self.subjects = []  # List to store subject references
        self.last_study_session = None
        self.study_streak = 0  # Track consecutive days of studying
        
    def add_subject(self, subject) -> None:
        """Add a subject to the player's list"""
        self.subjects.append(subject)
        
    def gain_exp(self, amount: int) -> None:
        """Gain experience points and level up if threshold reached"""
        self.exp += amount
        while self.exp >= self.get_exp_threshold():
            self.level_up()
            
    def level_up(self) -> None:
        """Level up the player and adjust exp"""
        self.level += 1
        self.exp -= self.get_exp_threshold()
        
    def get_exp_threshold(self) -> int:
        """Calculate exp needed for next level"""
        return self.level * 100  # Simple linear progression
        
    def record_study_session(self) -> None:
        """Record a study session and update streak"""
        now = datetime.now()
        if self.last_study_session:
            days_diff = (now - self.last_study_session).days
            if days_diff == 1:  # Consecutive day
                self.study_streak += 1
            elif days_diff > 1:  # Streak broken
                self.study_streak = 1
        else:
            self.study_streak = 1
        self.last_study_session = now
        
    def get_random_quote(self) -> str:
        """Get a random motivational quote from API"""
        try:
            response = requests.get("https://api.quotable.io/random?tags=education,motivation")
            if response.status_code == 200:
                data = response.json()
                return f"{data['content']} - {data['author']}"
        except:
            return "Knowledge is power!"  # Fallback quote
            
    def search_wikipedia(self, query: str) -> str:
        """Search Wikipedia for study notes"""
        try:
            # Using Wikipedia's API to get a summary
            response = requests.get(
                "https://en.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
            )
            if response.status_code == 200:
                return response.json()["extract"]
        except:
            return "Could not fetch information. Try a different search term."
            
    def to_dict(self) -> dict:
        """Convert player data to dictionary for JSON serialization"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'title': self.title,
            'email': self.email,
            'level': self.level,
            'exp': self.exp,
            'exp_to_next_level': self.get_exp_threshold() - self.exp,
            'study_streak': self.study_streak,
            'last_study_session': self.last_study_session.isoformat() if self.last_study_session else None,
            'subjects': [subject.to_dict() for subject in self.subjects]
        }

"""
magtry ka kung pano natin ma iimplement yung flash cards at notes

dun sa flashcards, feel ko mahirap hanapan ng Public APIs pero try ka pa din

sa notes naman, baka may mahanap ka kung pano maaccess ang
"""