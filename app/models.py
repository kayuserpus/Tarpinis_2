from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from datetime import datetime, timedelta

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Boolean, default=False)

    cart_items = db.relationship("Cart", back_populates="user", cascade="all, delete")
    orders = db.relationship("Order", back_populates="user", cascade="all, delete")
    transactions = db.relationship("Transaction", back_populates="user", cascade="all, delete")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)
    
    def lock_account(self, duration_minutes):
        self.locked_until = datetime.now() + timedelta(minutes=duration_minutes)
        self.failed_login_attempts = 0  

    def unlock_account(self):
        self.locked_until = None
        self.failed_login_attempts = 0 

    def is_account_locked(self):
        return self.locked_until is not None and self.locked_until > datetime.now()

    def increment_failed_login_attempts(self):
        self.failed_login_attempts += 1

class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String(500))
    category = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String(255), nullable=True)  # Add this line

    cart_items = db.relationship("Cart", back_populates="product", cascade="all, delete")
    order_items = db.relationship("OrderItem", back_populates="product", cascade="all, delete")
    discounts = db.relationship('Discount', back_populates='product', cascade="all, delete")

class Cart(db.Model):
    __tablename__ = 'Cart'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="cart_items")
    product = db.relationship("Product", back_populates="cart_items")

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    user = db.relationship("User", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete")

class OrderItem(db.Model):
    __tablename__ = 'OrderItems'
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship("Order", back_populates="order_items")
    product = db.relationship("Product", back_populates="order_items")

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    user = db.relationship("User", back_populates="transactions")

class Discount(db.Model):
    __tablename__ = 'Discounts'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)

    product = db.relationship('Product', back_populates='discounts')

    def __repr__(self):
        return f'<Product {self.product.name}>'
    