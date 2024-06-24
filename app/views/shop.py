from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Cart

shop_bp = Blueprint('shop', __name__)

@shop_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@shop_bp.route('/balance')
@login_required
def balance():
    return render_template('balance.html', balance=current_user.balance)

@shop_bp.route('/add_balance', methods=['POST'])
@login_required
def add_balance():
    amount = request.form.get('amount')
    
    try:
        current_user.balance += float(amount)
        db.session.commit()
        flash('Balance updated successfully.')
    except Exception as e:
        db.session.rollback()
        flash('Failed to update balance: ' + str(e))
    
    return redirect(url_for('shop.balance'))

@shop_bp.route('/cart')
@login_required
def cart():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', cart_items=cart_items)

@shop_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    quantity = request.form.get('quantity')
    product = Product.query.get_or_404(product_id)
    
    if product.quantity < int(quantity):
        flash('Not enough stock available.')
        return redirect(url_for('shop.index'))
    
    cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
    
    try:
        db.session.add(cart_item)
        db.session.commit()
        flash('Product added to cart.')
    except Exception as e:
        db.session.rollback()
        flash('Failed to add product to cart: ' + str(e))
    
    return redirect(url_for('shop.index'))

@shop_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    
    if current_user.balance < total:
        flash('Not enough balance.')
        return redirect(url_for('shop.cart'))
    
    for item in cart_items:
        item.product.quantity -= item.quantity
        db.session.delete(item)
    
    current_user.balance -= total
    
    try:
        db.session.commit()
        flash('Purchase successful.')
    except Exception as e:
        db.session.rollback()
        flash('Purchase failed: ' + str(e))
    
    return redirect(url_for('shop.cart'))