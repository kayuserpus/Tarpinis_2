from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from models import db, Item, Cart
from forms import CartForm

shop_bp = Blueprint('shop', __name__)

@shop_bp.route("/")
def shop_index():
    items = Item.query.all()
    form = CartForm()  
    return render_template('shared/shop.html', products=items, form=form)

# @shop_bp.route("/products")
# @login_required
# def products():
#     products = Product.query.all()
#     return render_template("products.html", products=products)

# @shop_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
# @login_required
# def add_to_cart(product_id):
#     quantity = int(request.form.get("quantity", 1))
#     product = Product.query.get_or_404(product_id)
    
#     if product.quantity < quantity:
#         flash('Not enough stock available.', 'danger')
#         return redirect(url_for('shop.products'))
    
#     cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
#     if cart_item:
#         cart_item.quantity += quantity
#     else:
#         cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
#         db.session.add(cart_item)
    
#     product.quantity -= quantity
#     db.session.commit()
#     flash('Item added to cart.', 'success')
#     return redirect(url_for('shop.cart'))

# @shop_bp.route("/cart")
# @login_required
# def cart():
#     cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
#     total = sum(item.product.price * item.quantity for item in cart_items)
#     return render_template("cart.html", cart_items=cart_items, total=total)

# @shop_bp.route("/checkout")
# @login_required
# def checkout():
#     cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
#     total = sum(item.product.price * item.quantity for item in cart_items)
#     return render_template("checkout.html", cart_items=cart_items, total=total)

# @shop_bp.route("/process_payment", methods=["POST"])
# @login_required
# def process_payment():
#     payment_method = request.form.get("payment_method")
#     cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
#     total = sum(item.product.price * item.quantity for item in cart_items)
    
#     order = Order(user_id=current_user.id, total_amount=total)
#     db.session.add(order)
#     db.session.commit()
    
#     for item in cart_items:
#         transaction = Transaction(order_id=order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price)
#         db.session.add(transaction)
#         db.session.delete(item)
    
#     db.session.commit()
    
#     if payment_method == "card":
#         # Implement payment by card logic here
#         flash('Payment by card processed successfully.', 'success')
#     elif payment_method == "cod":
#         # Implement payment on delivery logic here
#         flash('Order placed successfully. Pay on delivery.', 'success')
    
#     return redirect(url_for('shop.products'))
