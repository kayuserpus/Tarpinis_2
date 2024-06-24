from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Discount, User
from app.forms import ProductForm, DiscountForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    return render_template('admin.html')

@admin_bp.route('/admin/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, price=form.price.data, quantity=form.quantity.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('add_product.html', form=form)

@admin_bp.route('/admin/set_discount', methods=['GET', 'POST'])
@login_required
def set_discount():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    form = DiscountForm()
    if form.validate_on_submit():
        product = Product.query.get(form.product_id.data)
        if product:
            discount = Discount(product_id=product.id, discount_percentage=form.discount_percentage.data)
            db.session.add(discount)
            db.session.commit()
            flash('Discount set successfully.')
        else:
            flash('Product not found.')
    return render_template('set_discount.html', form=form)

@admin_bp.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized access"}), 403
    
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({"error": "Missing data"}), 400
    
    user = User(username=username, email=email)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/admin/get_user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    if not current_user.is_admin:
        return jsonify({"error": "Unauthorized access"}), 403
    
    user = User.query.get_or_404(user_id)
    
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "balance": user.balance,
        "is_admin": user.is_admin,
        "created_at": user.created_at
    }
    
    return jsonify(user_data), 200
