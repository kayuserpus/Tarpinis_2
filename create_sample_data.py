import os
from app import create_app, db, create_admin_user
from app.models import User, Product, Cart, Order, OrderItem, Transaction, Discount
from werkzeug.security import generate_password_hash
from datetime import datetime
from flask_migrate import upgrade
from dotenv import load_dotenv

# Set environment variables programmatically
os.environ['ADMIN_USERNAME'] = 'your_admin_username'
os.environ['ADMIN_EMAIL'] = 'your_admin_email'
os.environ['ADMIN_PASSWORD'] = 'your_admin_password'

load_dotenv()

def create_sample_data():
    app = create_app()
    app.app_context().push()

    # Run migrations to create the database schema
    upgrade()

    # Clear the database tables
    db.drop_all()
    db.create_all()

    # Create admin user
    create_admin_user()

    # Create users
    user1 = User(
        username='john_doe',
        email='john@example.com',
        password_hash=generate_password_hash('password123'),
        balance=100.0
    )
    db.session.add(user1)

    user2 = User(
        username='jane_doe',
        email='jane@example.com',
        password_hash=generate_password_hash('password123'),
        balance=150.0
    )
    db.session.add(user2)

    # Create products
    products = [
        {
            "name": "Apple",
            "price": 0.5,
            "quantity": 100,
            "description": "Fresh and juicy apples.",
            "image_path": "assets/images/product_images/apple.jpg"
        },
        {
            "name": "Banana",
            "price": 0.3,
            "quantity": 150,
            "description": "Ripe bananas rich in potassium.",
            "image_path": "assets/images/product_images/banana.jpg"
        },
        {
            "name": "Orange",
            "price": 0.7,
            "quantity": 120,
            "description": "Sweet and tangy oranges.",
            "image_path": "assets/images/product_images/orange.jpg"
        },
        {
            "name": "Milk_Rokiskio",
            "price": 1.5,
            "quantity": 50,
            "description": "Fresh whole milk.",
            "image_path": "assets/images/product_images/milk.jpg"
        },
        {
            "name": "Eggs_IKI",
            "price": 2.0,
            "quantity": 80,
            "description": "Organic eggs, pack of 12.",
            "image_path": "assets/images/product_images/eggs.jpg"
        },
        {
            "name": "Bread_Agota",
            "price": 1.2,
            "quantity": 60,
            "description": "Whole grain bread loaf.",
            "image_path": "assets/images/product_images/bread.jpg"
        },
        {
            "name": "Apple Juice",
            "price": 3.0,
            "quantity": 40,
            "description": "Fresh apple juice, 1 liter.",
            "image_path": "assets/images/product_images/apple_juice.jpg"
        },
        {
            "name": "Wine_Charlize",
            "price": 10.0,
            "quantity": 30,
            "description": "Fine red wine, 750ml bottle.",
            "image_path": "assets/images/product_images/wine.jpg"
        },
        {
            "name": "Carrot",
            "price": 0.2,
            "quantity": 200,
            "description": "Crunchy organic carrots.",
            "image_path": "assets/images/product_images/carrot.jpg"
        },
        {
            "name": "Chips Estrella",
            "price": 1.8,
            "quantity": 75,
            "description": "Crispy potato chips from Estrella.",
            "image_path": "assets/images/product_images/chips_estrella.jpg"
        },
        {
            "name": "Vanilla Ice Cream",
            "price": 4.5,
            "quantity": 50,
            "description": "Creamy vanilla ice cream, 500ml.",
            "image_path": "assets/images/product_images/vanilla_icecream.jpg"
        },
        {
            "name": "Mint Chewing Gum",
            "price": 0.99,
            "quantity": 100,
            "description": "Refreshing mint chewing gum, pack of 10.",
            "image_path": "assets/images/product_images/mint_chewing_gum.jpg"
        }
    ]

    for product_data in products:
        product = Product(
            name=product_data['name'].replace('_', ' '),
            price=product_data['price'],
            quantity=product_data['quantity'],
            description=product_data['description'],
            image_path=product_data['image_path']
        )
        db.session.add(product)
        db.session.flush()

        # Create cart items
        cart_item = Cart(
            user_id=user1.user_id,
            product_id=product.id,
            quantity=5
        )
        db.session.add(cart_item)

        # Create order
        order = Order(
            user_id=user1.user_id,
            total=product.price * 5,
            order_date=datetime.now()
        )
        db.session.add(order)
        db.session.flush()

        # Create order items
        order_item = OrderItem(
            order_id=order.order_id,
            product_id=product.id,
            quantity=5,
            price=product.price
        )
        db.session.add(order_item)

    # Create transactions
    transaction1 = Transaction(
        user_id=user1.user_id,
        amount=50.0,
        transaction_date=datetime.now()
    )
    db.session.add(transaction1)

    transaction2 = Transaction(
        user_id=user2.user_id,
        amount=75.0,
        transaction_date=datetime.now()
    )
    db.session.add(transaction2)

    # Create discounts
    discount1 = Discount(
        product_id=1,
        discount_percentage=10.0
    )
    db.session.add(discount1)

    db.session.commit()

    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()
