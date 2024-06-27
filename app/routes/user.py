from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Item, Cart, Order
from forms import BalanceForm, CartForm, PasswordChangeForm, ChangeEmailForm
from . import user
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

@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('users/account.html', user = current_user)


@user_bp.route('/orders_history', methods=['GET', 'POST'])
@login_required
def order_history():
    data = Order.query.filter_by(user_id=current_user.user_id).all()
    if not data:
        flash("No order history available.")
    return render_template('users/order_history.html', orders=data)
    
@user_bp.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    if request.method == 'POST':
        new_username = request.form.get('username') 
        if not new_username:
            flash('Please provide a new username.', 'danger')
            return redirect(url_for('user.change_username'))
        existing_user = User.query.filter_by(username=new_username).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'danger')
        else:
            current_user.username = new_username  
            db.session.commit()
            flash('Username successfully changed.', 'success')
    return render_template('users/change_username.html')

@user_bp.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        new_email = request.form.get('email')

        if not new_email:
            flash('Please provide an email address.', 'danger')
            return redirect(url_for('user.change_email'))

        if User.query.filter_by(email=new_email).first():
            flash('Email already taken. Please choose a different one.', 'danger')
        else:
            current_user.email = new_email
            db.session.commit()
            flash('Email successfully changed.', 'success')
        
    return render_template('users/change_email.html')

@user_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if not current_user.check_password(form.old_password.data):
                flash('Incorrect old password.', 'danger')
            else:
                current_user.set_password(form.new_password.data)
                db.session.commit()
                flash('Password successfully changed.', 'success')
                return redirect(url_for('user.account'))
        else:
            flash('Please fill in all fields.\n New password and confirmation should match.', 'danger')
    return render_template('users/change_password.html', form=form)

