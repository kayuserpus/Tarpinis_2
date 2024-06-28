from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from forms import LoginForm, RegistrationForm
from app.models import User
from datetime import datetime, timedelta
import re

auth_bp = Blueprint('auth', __name__)
locked_users = {}
login_attempts = {}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'error')
            increment_failed_login_attempts(username)
            
            failed_attempts = get_failed_login_attempts(username)
            if failed_attempts >= 3:
                lockout_duration = 5 if failed_attempts == 3 else 15 if failed_attempts == 4 else 60
                lock_account(username, lockout_duration) 
                flash(f'Account locked for {lockout_duration} minutes.', 'error')

            return redirect(url_for('auth.login'))

        reset_failed_login_attempts(username)
        clear_lockout(username) 
        login_user(user)
        if user.is_admin:
            return redirect(url_for('admin.admin_dashboard'))
        else:
            return redirect(url_for('user.shop'))
            

    return render_template('auth/login.html', form=form)

def increment_failed_login_attempts(username):
    login_attempts[username] = login_attempts.get(username, 0) + 1

def get_failed_login_attempts(username):
    return login_attempts.get(username, 0)

def reset_failed_login_attempts(username):
    if username in login_attempts:
        del login_attempts[username]

def lock_account(username, duration_minutes):
    locked_users[username] = datetime.now() + timedelta(minutes=duration_minutes)

def is_account_locked(username):
    return username in locked_users and locked_users[username] > datetime.now()

def get_lockout_duration(username):
    if username in locked_users:
        delta = locked_users[username] - datetime.now()
        return int(delta.total_seconds() / 60) 
    return 0

def clear_lockout(username):
    if username in locked_users:
        del locked_users[username]

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm.data
            
            errors = []
            
            if not username:
                errors.append('Username is required.')
            
            if not email:
                errors.append('Email is required.')
            elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
                errors.append('Invalid email format. Must be in the format name@domain.com.')
            
            if not password:
                errors.append('Password is required.')
            elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
                errors.append('Password must be at least 8 characters long, include letters and numbers.')
            
            if password != confirm_password:
                errors.append('Passwords do not match.')
            
            if User.query.filter_by(username=username).first():
                errors.append('Username already taken. Please choose a different one.')

            if User.query.filter_by(email=email).first():
                errors.append('Email address already registered. Please use a different one.')

            if errors:
                for error in errors:
                    flash(error, 'error')
                return render_template('auth/register.html', form=form)
            
            user = User(username=username, email=email)
            user.set_password(password)
            
            try:
                db.session.add(user)
                db.session.commit()
                flash('Registration successful. Please log in.')
                return redirect(url_for('auth.login'))
            except Exception as e:
                db.session.rollback()
                flash('Registration failed: ' + str(e), 'error')
                return render_template('auth/register.html', form=form)
    
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/test')
def test():
    return render_template('auth/login.html')

