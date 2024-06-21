"""Added some sample data

Revision ID: 97cdb1d8d38c
Revises: d0672b1e1bcf
Create Date: 2024-06-21 13:39:04.273476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97cdb1d8d38c'
down_revision: Union[str, None] = 'd0672b1e1bcf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Insert sample users
    op.execute("""
    INSERT INTO Users (username, password, email, balance, is_admin) VALUES 
    ('john_doe', 'password123', 'john@example.com', 100.0, 0),
    ('jane_smith', 'password123', 'jane@example.com', 150.0, 0),
    ('admin_user', 'adminpass', 'admin@example.com', 0.0, 1);
    """)
    
    # Insert sample items
    op.execute("""
    INSERT INTO Items (name, description, price, stock) VALUES 
    ('Apple', 'Fresh Red Apple', 0.50, 100),
    ('Banana', 'Organic Bananas', 0.30, 200),
    ('Milk', '1 Liter Full Cream Milk', 1.20, 50),
    ('Bread', 'Whole Wheat Bread', 2.50, 30);
    """)
    
    # Insert sample carts
    op.execute("""
    INSERT INTO Cart (user_id, item_id, quantity) VALUES 
    (1, 1, 5),  -- john_doe buys 5 apples
    (1, 3, 2),  -- john_doe buys 2 milk
    (2, 2, 10); -- jane_smith buys 10 bananas
    """)
    
    # Insert sample orders with correct datetime
    op.execute("""
    INSERT INTO Orders (user_id, total, order_date) VALUES 
    (1, 4.20, datetime('now')),  -- john_doe places an order
    (2, 3.00, datetime('now'));  -- jane_smith places an order
    """)
    
    # Insert sample order items
    op.execute("""
    INSERT INTO OrderItems (order_id, item_id, quantity, price) VALUES 
    (1, 1, 5, 2.50),  -- 5 apples for john_doe's order
    (1, 3, 2, 2.40),  -- 2 milk for john_doe's order
    (2, 2, 10, 3.00); -- 10 bananas for jane_smith's order
    """)
    
    # Insert sample transactions with correct datetime
    op.execute("""
    INSERT INTO Transactions (user_id, amount, transaction_date) VALUES 
    (1, -4.20, datetime('now')),  -- john_doe's order deduction
    (2, -3.00, datetime('now'));  -- jane_smith's order deduction
    """)


def downgrade() -> None:
    # Optionally, delete the inserted data if you need to revert the migration
    op.execute("DELETE FROM Transactions;")
    op.execute("DELETE FROM OrderItems;")
    op.execute("DELETE FROM Orders;")
    op.execute("DELETE FROM Cart;")
    op.execute("DELETE FROM Items;")
    op.execute("DELETE FROM Users;")
