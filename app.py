import os
from flask import Flask, redirect, url_for
from config import Config
from extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register blueprints
    from routes.user import user_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp 
    from routes.shop import shop_bp

    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
