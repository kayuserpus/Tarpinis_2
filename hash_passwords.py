from werkzeug.security import generate_password_hash
from extensions import db
from models import User
from app import create_app
from config import Config  # Ensure this import is correct

app = create_app()

with app.app_context():
    users = User.query.all()
    for user in users:
        print(f"Hashing password for user: {user.username}")
        if not user.password.startswith('pbkdf2:sha256'):  # Check if the password is already hashed
            hashed_password = generate_password_hash(user.password)
            print(f"Old password: {user.password}, New hashed password: {hashed_password}")
            user.password = hashed_password
    db.session.commit()
    db.session.flush()
    db.session.expire_all()
    print("Password hashing completed and changes committed to the database.")
