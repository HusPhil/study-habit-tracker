# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cram_quest.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'admin'  # for session management