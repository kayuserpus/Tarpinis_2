# app.py

from flask import Flask, render_template
from crud.user import get_all_users
from database import create_app, db

app = create_app()

@app.route("/users")
def users():
    users = get_all_users()
    return render_template("users/index.html", arr=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
