from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Discount, User
from forms import ProductForm, DiscountForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    return render_template('admin/admin.html')

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
    return render_template('admin/add_product.html', form=form)

@admin_bp.route('/admin/update_product_quantity/<int:product_id>', methods=['POST'])
@login_required
def update_product_quantity(product_id):
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('user.shop'))
    product = Product.query.get_or_404(product_id)
    quantity = request.form.get('quantity')
    if quantity is not None:
        product.quantity = int(quantity)
        db.session.commit()
        flash('Product quantity updated successfully.', 'success')
    else:
        flash('Invalid data.', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/remove_product/<int:product_id>', methods=['POST'])
@login_required
def remove_product(product_id):
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('user.shop'))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product removed successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

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
    return render_template('admin/set_discount.html', form=form)

def update_discount(discount_id):
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('user.shop'))
    discount = Discount.query.get_or_404(discount_id)
    form = DiscountForm(obj=discount)
    if form.validate_on_submit():
        discount.discount_percentage = form.discount_percentage.data
        db.session.commit()
        flash('Discount updated successfully.', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('update_discount.html', form=form)

@admin_bp.route('/admin/remove_discount/<int:discount_id>', methods=['POST'])
@login_required
def remove_discount(discount_id):
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('user.shop'))
    discount = Discount.query.get_or_404(discount_id)
    db.session.delete(discount)
    db.session.commit()
    flash('Discount removed successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.shop'))
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not username or not email or not password:
        flash('Missing data.', 'danger')
        return redirect(url_for('admin.admin_dashboard'))
    user = User(username=username, email=email)
    user.set_password(password)
    try:
        db.session.add(user)
        db.session.commit()
        flash('User created successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/admin/get_user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.shop'))
    user = User.query.get_or_404(user_id)
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "balance": user.balance,
        "is_admin": user.is_admin,
        "created_at": user.created_at
    }
    return render_template('user_details.html', user=user_data)

@admin_bp.route('/admin/remove_user/<int:user_id>', methods=['POST'])
@login_required
def remove_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.shop'))
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User removed successfully.', 'success')
    return redirect(url_for('admin.admin_dashboard'))
