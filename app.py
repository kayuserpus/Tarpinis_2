# app.py

from flask import Flask, render_template
from crud.user import get_all_users
from crud.orders import get_all_orders
from database import create_app, db

app = create_app()

@app.route("/users")
def users():
    users = get_all_users()
    return render_template("users/index.html", arr=users)

@app.route("/orders")
def orders():
    data = get_all_orders()
    return render_template("orders/index.html", arr=data)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
