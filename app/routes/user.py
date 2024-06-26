from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Item, Cart, Order, Transaction, OrderItem
from forms import BalanceForm, CartForm
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/shop')
def shop():
    items = Item.query.all()
    form = CartForm()  
    return render_template('shared/index.html', products=items, form=form)

@user_bp.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = BalanceForm()
    error = None
    if form.validate_on_submit():
        try:
            amount = float(form.amount.data)
            if amount <= 0:
                error = "Amount must be positive."
            else:
                current_user.balance += amount
                db.session.commit()
                flash('Balance updated successfully!', 'success')
                return redirect(url_for('user.balance'))
        except ValueError:
            error = "Invalid input. Please enter a numeric value."
        except Exception as e:
            error = str(e)
    return render_template('users/balance.html', form=form, error=error)

@user_bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render_template('users/cart.html', cart_items=cart_items, total=total)


@user_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if not current_user.is_authenticated:
        flash('You need to be logged in to add items to the cart.', 'warning')
        return redirect(url_for('auth.login'))

    form = CartForm()
    if form.validate_on_submit():
        item = Item.query.get(form.product_id.data)
        if item and item.stock >= form.quantity.data:
            cart_item = Cart.query.filter_by(user_id=current_user.user_id, item_id=item.item_id).first()
            if cart_item:
                cart_item.quantity += form.quantity.data
            else:
                cart_item = Cart(user_id=current_user.user_id, item_id=item.item_id, quantity=form.quantity.data)
                db.session.add(cart_item)
            item.stock -= form.quantity.data
            db.session.commit()
            flash('Item added to cart.')
        else:
            flash('Item not available in the requested quantity.', 'error')
    return redirect(url_for('user.shop'))

@user_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    total = sum(item.item.price * item.quantity for item in cart_items)
    
    if current_user.balance >= total:
        # Step 1: Create and commit the Order record
        order = Order(user_id=current_user.user_id, total=total)
        db.session.add(order)
        db.session.commit()
        
        # Step 2: Retrieve the order_id from the committed Order record
        order_id = order.order_id

        # Step 3: Create and add OrderItems records using the retrieved order_id
        for item in cart_items:
            order_item = OrderItem(order_id=order_id, item_id=item.item_id, quantity=item.quantity, price=item.item.price)
            db.session.add(order_item)

        # Step 4: Commit the OrderItems records
        db.session.commit()

        # Remove items from cart and update user balance
        for item in cart_items:
            db.session.delete(item)
        current_user.balance -= total
        db.session.commit()
        
        flash('Purchase successful.', 'success')
    else:
        flash('Insufficient balance.', 'danger')
        
    return redirect(url_for('user.cart'))


@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('users/account.html', user = current_user)


@user_bp.route('/orders_history', methods=['GET', 'POST'])
@login_required
def order_history():
    data = Order.query.filter_by(user_id=current_user.user_id).all()
    return render_template('users/orders_history.html', arr = data)

@user_bp.route('/create_order', methods=['POST'])
@login_required
def create_order():
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    if not cart_items:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('user.cart'))

    total = sum(item.item.price * item.quantity for item in cart_items)

    if current_user.balance < total:
        flash('Insufficient balance.', 'danger')
        return redirect(url_for('user.cart'))

    try:
        # Create a new order
        new_order = Order(user_id=current_user.user_id, total=total)
        db.session.add(new_order)
        db.session.commit()  # Commit to get the order_id

        # Add items to the order
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=new_order.order_id,
                item_id=cart_item.item_id,
                quantity=cart_item.quantity,
                price=cart_item.item.price
            )
            db.session.add(order_item)
            db.session.delete(cart_item)  # Remove the item from the cart

        # Deduct the total from the user's balance
        current_user.balance -= total
        db.session.commit()

        flash('Order created successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('user.order_history'))
