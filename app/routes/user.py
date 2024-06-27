from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import User, Product, Cart, Order, OrderItem
from forms import BalanceForm, CartForm
from app import db
from datetime import timedelta
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
    form = CartForm()
    cart_items = Cart.query.filter_by(user_id=current_user.user_id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('users/cart.html', cart_items=cart_items, total=total, form=form)


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
    if not cart_items:
        flash('Your cart is empty. Please add items to your cart before checkout.', 'warning')
        return redirect(url_for('user.cart'))
    total = sum(item.product.price * item.quantity for item in cart_items)
    if current_user.balance < total:
        flash('Insufficient balance. Please add funds to your account.', 'danger')
        return redirect(url_for('user.cart'))
    try:
        order = Order(user_id=current_user.user_id, total=total)
        db.session.add(order)
        db.session.commit()
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            item.product.quantity -= item.quantity
        Cart.query.filter_by(user_id=current_user.user_id).delete()
        db.session.commit()
        current_user.balance -= total
        db.session.commit()
        flash('Purchase successful. Your order has been placed.', 'success')
    except Exception as e:
        flash(f'An error occurred: {str(e)}', 'danger')
    return redirect(url_for('user.cart'))


@user_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('users/account.html', user=current_user)

@user_bp.route('/orders_history', methods=['GET'])
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.user_id).all()
    for order in orders:
        order.order_date += timedelta(hours=3)
    return render_template('users/orders_history.html', orders=orders)




@user_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').strip().lower()
    if query:
        results = Product.query.filter(Product.name.ilike(f'%{query}%')).all()
    else:
        results = []
    form = CartForm()
    return render_template('shared/index.html', products=results, form=form)


@user_bp.route('/remove_one_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_one_from_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=current_user.user_id, product_id=item_id).first()
    if cart_item:
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            db.session.delete(cart_item)
        db.session.commit()
        flash('One item removed from cart.', 'success')
    else:
        flash('Item not found in cart.', 'danger')
    return redirect(url_for('user.cart'))

@user_bp.route('/remove_all_from_cart/<int:item_id>', methods=['POST'])
@login_required
def remove_all_from_cart(item_id):
    cart_item = Cart.query.filter_by(user_id=current_user.user_id, product_id=item_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('All items removed from cart.', 'success')
    else:
        flash('Item not found in cart.', 'danger')
    return redirect(url_for('user.cart'))
