from database import db
from models import Order

def get_all_orders():
    data = db.session.query(Order).all()
    return data
