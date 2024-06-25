from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Item, Cart
from forms import BalanceForm, CartForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/shop')
@login_required
def shop():
    items = Item.query.all()
    return render_template('shared/shop.html', products=items)

@user_bp.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = BalanceForm()
    error = None
    if form.validate_on_submit():
        try:
            amount = float(form.amount.data)
            # Update user's balance logic here
            current_user.balance += amount
            db.session.commit()  # Commit the changes to the database
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
    return render_template('cart.html', cart_items=cart_items, total=total)

@user_bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
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
            flash('Item not available in the requested quantity.')
    return redirect(url_for('user.shop'))

@user_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    total = sum(item.item.price * item.quantity for item in cart_items)
    if current_user.balance >= total:
        for item in cart_items:
            db.session.delete(item)
        current_user.balance -= total
        db.session.commit()
        flash('Purchase successful.')
    else:
        flash('Insufficient balance.')
    return redirect(url_for('user.cart'))
