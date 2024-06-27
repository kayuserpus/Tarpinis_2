from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, user_loaded_from_header
from dotenv import load_dotenv
import os
from config import Config  # Ensure this line is added

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.models import User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.user import user_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)

    return app

def create_admin_user():
    from app.models import User
    admin_username = os.environ.get('ADMIN_USERNAME')
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')

    if admin_username and admin_email and admin_password:
        admin = User.query.filter_by(username=admin_username).first()
        if not admin:
            admin = User(
                username=admin_username,
                email=admin_email,
                is_admin=True
            )
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
    else:
        raise ValueError("Environment variables ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD are not set.")
