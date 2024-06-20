from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, Product, CartItem
from app.forms import BalanceForm, CartForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/shop')
@login_required
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@user_bp.route('/balance', methods=['GET', 'POST'])
@login_required
def balance():
    form = BalanceForm()
    if form.validate_on_submit():
        current_user.balance += form.amount.data
        db.session.commit()
        flash('Your balance has been updated.')
        return redirect(url_for('user.balance'))
    return render_template('balance.html', form=form)

@user_bp.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@user_bp.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    form = CartForm()
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if product and product.quantity >= form.quantity.data:
            cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product.id).first()
            if cart_item:
                cart_item.quantity += form.quantity.data
            else:
                cart_item = CartItem(user_id=current_user.id, product_id=product.id, quantity=form.quantity.data)
                db.session.add(cart_item)
            product.quantity -= form.quantity.data
            db.session.commit()
            flash('Product added to cart.')
        else:
            flash('Product not available in the requested quantity.')
    return redirect(url_for('user.shop'))

@user_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
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
