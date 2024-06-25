import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your_secret_key_here' 
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, "database.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True 
