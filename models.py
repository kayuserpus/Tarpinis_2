from flask_login import UserMixin
from extensions import db

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    balance = db.Column(db.Float, default=0.0)
    is_admin = db.Column(db.Integer, default=0)

    def get_id(self):
        return self.user_id

class Item(db.Model):
    __tablename__ = 'Items'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    __tablename__ = 'Cart'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('Items.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    user = db.relationship("User", back_populates="cart_items")
    item = db.relationship("Item", back_populates="cart_items")

class Order(db.Model):
    __tablename__ = 'Orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    user = db.relationship("User", back_populates="orders")

class OrderItem(db.Model):
    __tablename__ = 'OrderItems'
    order_item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('Items.item_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    order = db.relationship("Order", back_populates="order_items")
    item = db.relationship("Item", back_populates="order_items")

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    user = db.relationship("User", back_populates="transactions")

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, default=0)
    description = db.Column(db.String(500))
 
class Discount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)
 
    product = db.relationship('Product', backref=db.backref('discounts', lazy=True)) 

    def __repr__(self):
        return f'<Product {self.name}>'
 

User.cart_items = db.relationship("Cart", back_populates="user")
User.orders = db.relationship("Order", back_populates="user")
User.transactions = db.relationship("Transaction", back_populates="user")
Item.cart_items = db.relationship("Cart", back_populates="item")
Item.order_items = db.relationship("OrderItem", back_populates="item")
Order.order_items = db.relationship("OrderItem", back_populates="order")
