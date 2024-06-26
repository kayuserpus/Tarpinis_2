from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Item, Cart, Order
from forms import BalanceForm, CartForm
from . import user
from forms import BalanceForm
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/shop', methods=['GET'])
def shop():
    selected_category = request.args.get('category', '')

    categories = db.session.query(Item.category.distinct()).all()
    categories = [category[0] for category in categories]

    if selected_category:
        items = Item.query.filter_by(category=selected_category).all()
    else:
        items = Item.query.all()  # Fetch all items if no category is selected

    form = CartForm()
    return render_template('shared/index.html', products=items, form=form, categories=categories, selected_category=selected_category)

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
    form = CartForm()
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    total = sum(item.item.price * item.quantity for item in cart_items)
    return render_template('users/cart.html', cart_items=cart_items, total=total, form=form)


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
    return render_template('users/orders_history.html', arr = data)


@user_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    if query:
        results = Item.query.filter(Item.name.ilike(f'%{query}%')).all()
    else:
        results = []
    form = CartForm()
    return render_template('shared/index.html', products=results, form=form)

@user_bp.route('/product/<product_id>')
def product_detail(product_id):
    product = Item.query.get_or_404(product_id)
    form = CartForm()
    return render_template('shared/product_detail.html', product=product, form=form)


@user_bp.route('/remove_one_from_cart/<item_id>', methods=['POST'])
@login_required
def remove_one_from_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=current_user.user_id, item_id=item_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            db.session.commit()
            flash('One quantity of the item removed from cart.', 'success')
        else:
            db.session.delete(cart_item)
            flash('Item removed from cart.', 'success')
        db.session.commit()
    return redirect(url_for('user.cart'))

@user_bp.route('/remove_all_from_cart/<item_id>', methods=['POST'])
@login_required
def remove_all_from_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=current_user.user_id, item_id=item_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('All quantities of the item removed from cart.', 'success')
    return redirect(url_for('user.cart'))