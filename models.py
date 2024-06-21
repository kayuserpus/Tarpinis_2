from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, TIMESTAMP, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///database.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    balance = Column(Float, default=0.0)
    is_admin = Column(Integer, default=0)

class Item(Base):
    __tablename__ = 'Items'
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

class Cart(Base):
    __tablename__ = 'Cart'
    cart_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('Items.item_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    user = relationship("User", back_populates="cart_items")
    item = relationship("Item", back_populates="cart_items")

class Order(Base):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    total = Column(Float, nullable=False)
    order_date = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    user = relationship("User", back_populates="orders")

class OrderItem(Base):
    __tablename__ = 'OrderItems'
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.order_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('Items.item_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")

class Transaction(Base):
    __tablename__ = 'Transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(TIMESTAMP, server_default='CURRENT_TIMESTAMP')
    user = relationship("User", back_populates="transactions")

User.cart_items = relationship("Cart", back_populates="user")
User.orders = relationship("Order", back_populates="user")
User.transactions = relationship("Transaction", back_populates="user")
Item.cart_items = relationship("Cart", back_populates="item")
Item.order_items = relationship("OrderItem", back_populates="item")
Order.order_items = relationship("OrderItem", back_populates="order")

metadata = Base.metadata
