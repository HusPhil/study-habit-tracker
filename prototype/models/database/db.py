import sqlite3
from typing import Any, List
from contextlib import contextmanager
import threading
from queue import Queue
import os

class ConnectionPool:
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self._local = threading.local()
        self.lock = threading.Lock()
    
    def _create_connection(self):
        """Create a new database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_connection(self):
        """Get a connection from the pool or create a new one if needed"""
        if not hasattr(self._local, 'connection'):
            self._local.connection = self._create_connection()
        
        try:
            yield self._local.connection
        except Exception as e:
            self._local.connection.rollback()
            raise e
        finally:
            self._local.connection.commit()

class Database:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.initialized = False
            return cls._instance

    def __init__(self):
        if not self.initialized:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'cram_quest.db')
            self.pool = ConnectionPool(db_path)
            self.setup_database()
            self.initialized = True

    def setup_database(self):
        with self.pool.get_connection() as conn:
            c = conn.cursor()
            
            # Users table with indexes
            c.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    level INTEGER DEFAULT 1,
                    exp INTEGER DEFAULT 0,
                    title TEXT DEFAULT 'Noobie'
                )
            ''')
            
            # Create indexes for frequent queries
            c.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
            c.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
            
            # Subjects table with indexes
            c.execute('''
                CREATE TABLE IF NOT EXISTS subjects (
                    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    difficulty INTEGER DEFAULT 1,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                )
            ''')
            c.execute('CREATE INDEX IF NOT EXISTS idx_subjects_user ON subjects(user_id)')
                
            # Quests table with indexes
            c.execute('''
                CREATE TABLE IF NOT EXISTS quests (
                    quest_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    difficulty INTEGER DEFAULT 1,
                    status INTEGER DEFAULT 0,
                    subject_id INTEGER,
                    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
                )
            ''')
            c.execute('CREATE INDEX IF NOT EXISTS idx_quests_subject ON quests(subject_id)')

            c.execute('''
                CREATE TABLE IF NOT EXISTS badges (    
                    badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    description TEXT NOT NULL,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            ''')
                    

            c.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    note_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_id INTEGER,
                    description TEXT NOT NULL,
                    link TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE
                )
            ''')

            c.execute('''
                CREATE TABLE IF NOT EXISTS flashcards (
                    flashcard_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    subject_id INTEGER,
                    description TEXT NOT NULL,
                    link TEXT NOT NULL,
                    status INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (subject_id) REFERENCES subjects (subject_id) ON DELETE CASCADE
                )
            ''')



            

    def execute(self, query: str, params: tuple = ()) -> List[sqlite3.Row]:
        """Execute a query with thread-safe connection handling"""
        with self.pool.get_connection() as conn:
            try:
                c = conn.cursor()
                c.execute(query, params)
                return c.fetchall()
            except sqlite3.Error as e:
                raise DatabaseError(f"Database error: {str(e)}")

    def execute_many(self, query: str, params_list: List[tuple]) -> None:
        """Execute many queries with thread-safe connection handling"""
        with self.pool.get_connection() as conn:
            try:
                c = conn.cursor()
                c.executemany(query, params_list)
            except sqlite3.Error as e:
                raise DatabaseError(f"Database error: {str(e)}")

class DatabaseError(Exception):
    """Custom exception for database errors"""
    pass

# Global database instance
db = Database()

# Ewan ko talaga tong part na tong dalwa, nilagay ko lang baka kelangan, bobo ko sa db hayss
def add_badge(title: str, rarity: str) -> int:
    """Add a new badge to the badges table and return its ID."""
    query = "INSERT INTO badges (title, rarity) VALUES (?, ?)"
    db.execute(query, (title, rarity))
    badge_id = db.execute("SELECT last_insert_rowid() AS id")[0]["id"]
    return badge_id

def add_badge_to_player(player_id: int, badge_id: int):
    """Associate a badge with a player."""
    query = "INSERT INTO player_badges (player_id, badge_id) VALUES (?, ?)"
    db.execute(query, (player_id, badge_id))