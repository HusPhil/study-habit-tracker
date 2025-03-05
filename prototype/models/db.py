# models/db.py
import sqlite3
from typing import Dict, List, Any
from datetime import datetime

class Database:
    def __init__(self, db_name: str = "study_quest.db"):
        self.db_name = db_name
        self.setup_database()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def setup_database(self):
        conn = self.get_connection()
        c = conn.cursor()
        
        # Create users table
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                type TEXT NOT NULL,
                title TEXT,
                level INTEGER,
                exp INTEGER,
                study_streak INTEGER,
                last_study_session TEXT
            )
        ''')
        
        # Create subjects table
        c.execute('''
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                difficulty INTEGER,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def execute(self, query: str, params: tuple = None) -> Any:
        conn = self.get_connection()
        c = conn.cursor()
        if params:
            c.execute(query, params)
        else:
            c.execute(query)
        result = c.fetchall()
        conn.commit()
        conn.close()
        return result

db = Database()