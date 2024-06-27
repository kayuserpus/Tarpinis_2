from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Product, Cart, Order
from forms import BalanceForm, CartForm
from app import db
from app.helpers import get_products_and_categories

user_bp = Blueprint('user', __name__)

@user_bp.route('/shop', methods=['GET'])
def shop():
    selected_category = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    products, categories = get_products_and_categories(selected_category, search_query)
    form = CartForm()
    return render_template('shared/index.html', products=products, form=form, categories=categories, selected_category=selected_category)

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
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('users/cart.html', cart_items=cart_items, total=total)

@user_bp.route('/add_to_cart', methods=['GET'])
def add_to_cart():
    if not current_user.is_authenticated:
        flash('You need to be logged in to add items to the cart.', 'warning')
        return redirect(url_for('auth.login'))

    product_id = request.args.get('product_id', type=int)
    quantity = request.args.get('quantity', type=int, default=1)

    if not product_id or not quantity:
        flash('Invalid input.', 'danger')
        return redirect(url_for('user.shop'))

    product = Product.query.get(product_id)
    if product and product.quantity >= quantity:
        cart_item = Cart.query.filter_by(user_id=current_user.user_id, product_id=product.id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = Cart(user_id=current_user.user_id, product_id=product.id, quantity=quantity)
            db.session.add(cart_item)
        product.quantity -= quantity
        db.session.commit()
        flash('Item added to cart.')
    else:
        flash('Item not available in the requested quantity.')
    
    return redirect(url_for('user.shop'))

@user_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
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
    return render_template('users/account.html', user=current_user)

@user_bp.route('/orders_history', methods=['GET', 'POST'])
@login_required
def order_history():
    data = Order.query.filter_by(user_id=current_user.user_id).all()
    return render_template('users/orders_history.html', orders=data)
