# crud/user.py

from database import db
from models import User

def get_all_users():
    users = db.session.query(User).all()
    return users
