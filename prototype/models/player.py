# models/player.py
from .user import User
from datetime import datetime
import requests
from .db import db

class Player(User):
    def __init__(self, user_id: int, email: str, username: str, password: str, 
                 level: int = 1, exp: int = 0, title: str = "Noobie"):
        super().__init__(user_id, email, username, password)
        self.title = title
        self.level = level
        self.exp = exp
        self.subjects = []
        self.last_study_session = None
        self.study_streak = 0

    @staticmethod
    def create(email: str, username: str, password: str) -> 'Player':
        """Create a new player in database"""
        query = """
            INSERT INTO users 
            (email, username, password, type, title, level, exp, study_streak) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        db.execute(query, (email, username, password, 'player', 
                         "Noobie", 1, 0, 0))
        # Get the created player
        result = db.execute("SELECT user_id FROM users WHERE email = ?", (email,))
        user_id = result[0][0]
        return Player(user_id, email, username, password)

    @staticmethod
    def get(user_id: int) -> 'Player':
        """Get player from database"""
        result = db.execute("SELECT * FROM users WHERE user_id = ? AND type = 'player'", (user_id,))
        if result:
            data = result[0]
            player = Player(
                user_id=data[0], 
                email=data[1], 
                username=data[2], 
                password=data[3],
                title=data[5],
                level=data[6],
                exp=data[7]
            )
            player.study_streak = data[8]
            if data[9]:  # last_study_session
                player.last_study_session = datetime.fromisoformat(data[9])
            # Load subjects
            subjects = db.execute("SELECT * FROM subjects WHERE user_id = ?", (user_id,))
            player.subjects = [Subject(*s) for s in subjects]
            return player
        return None

    def save(self) -> None:
        """Save changes to database"""
        query = """
            UPDATE users 
            SET email = ?, username = ?, password = ?, title = ?, 
                level = ?, exp = ?, study_streak = ?, 
                last_study_session = ?
            WHERE user_id = ?
        """
        last_session = self.last_study_session.isoformat() if self.last_study_session else None
        db.execute(query, (
            self.email, self.username, self._User__password, 
            self.title, self.level, self.exp, 
            self.study_streak, last_session, self.user_id
        ))

    def gain_exp(self, amount: int) -> None:
        """Gain experience points and level up if threshold reached"""
        self.exp += amount
        while self.exp >= self.get_exp_threshold():
            self.level_up()
        self.save()  # Save changes to database
            
    def level_up(self) -> None:
        """Level up the player and adjust exp"""
        self.level += 1
        self.exp -= self.get_exp_threshold()
        self.save()  # Save changes to database
        
    def get_exp_threshold(self) -> int:
        """Calculate exp needed for next level"""
        return self.level * 100
        
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
        self.save()  # Save changes to database
        
    def get_random_quote(self) -> str:
        """Get a random motivational quote from API"""
        try:
            response = requests.get("https://api.quotable.io/random?tags=education,motivation")
            if response.status_code == 200:
                data = response.json()
                return f"{data['content']} - {data['author']}"
        except:
            return "Knowledge is power!"