from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Product, Discount, User
from forms import ProductForm, DiscountForm, UserForm
import os
from flask import current_app
from werkzeug.utils import secure_filename

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
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.root_path, 'static/assets/images/product_images', filename)
            image_file.save(image_path)
            product = Product(
                name=form.name.data,
                price=form.price.data,
                quantity=form.quantity.data,
                description=form.description.data,
                image_path=f'assets/images/product_images/{filename}'
            )
        else:
            product = Product(
                name=form.name.data, 
                price=form.price.data, 
                quantity=form.quantity.data, 
                description=form.description.data
            )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.')
        return redirect(url_for('admin.list_products'))
    
    return render_template('admin/add_product.html', form=form)

@admin_bp.route('/admin/products')
@login_required
def list_products():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    products = Product.query.all()
    return render_template('admin/list_products.html', products=products)

@admin_bp.route('/admin/update_product_quantity/<int:product_id>', methods=['GET', 'POST'])
@login_required
def update_product_quantity(product_id):
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('user.shop'))
    
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        product.quantity = form.quantity.data
        db.session.commit()
        flash('Product quantity updated successfully.', 'success')
        return redirect(url_for('admin.list_products'))
    
    return render_template('admin/update_product_quantity.html', form=form, product_id=product_id)

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
    return redirect(url_for('admin.list_products'))

@admin_bp.route('/admin/set_discount', methods=['GET', 'POST'])
@login_required
def set_discount():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    
    form = DiscountForm()
    
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        discount_percentage = request.form.get('discount_percentage')
        
        if product_id and discount_percentage:
            try:
                product_id = int(product_id)
                discount_percentage = float(discount_percentage)
                
                product = Product.query.get(product_id)
                if product:
                    discount = Discount(product_id=product.id, discount_percentage=discount_percentage)
                    db.session.add(discount)
                    db.session.commit()
                    flash('Discount set successfully.')
                    return redirect(url_for('admin.list_discounts'))
                else:
                    flash('Product not found.')
            except ValueError:
                flash('Invalid input. Please enter valid data.')
        else:
            flash('All fields are required.')
    
    return render_template('admin/set_discount.html', form=form)

@admin_bp.route('/admin/discounts')
@login_required
def list_discounts():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    discounts = Discount.query.all()
    return render_template('admin/list_discounts.html', discounts=discounts)

@admin_bp.route('/admin/update_discount/<int:discount_id>', methods=['GET', 'POST'])
@login_required
def update_discount(discount_id):
    if not current_user.is_admin:
        flash('Admin access required.', 'danger')
        return redirect(url_for('user.shop'))
    discount = Discount.query.get_or_404(discount_id)
    discount_percentage = request.form.get('discount_percentage')
    if discount_percentage is not None:
        discount.discount_percentage = float(discount_percentage)
        db.session.commit()
        flash('Discount updated successfully.', 'success')
    else:
        flash('Invalid data.', 'danger')
    return redirect(url_for('admin.list_discounts'))

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
    return redirect(url_for('admin.list_discounts'))

@admin_bp.route('/admin/create_user', methods=['GET', 'POST'])
@login_required
def create_user():
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.shop'))
    
    form = UserForm()
    form.submit.label.text = 'Create User'
    if request.method == 'POST':
        if form.validate_on_submit():
            existing_user = User.query.filter((User.username == form.username.data) | (User.email == form.email.data)).first()
            if existing_user:
                if existing_user.username == form.username.data:
                    flash('Username already taken. Please choose a different one.', 'danger')
                if existing_user.email == form.email.data:
                    flash('Email address already registered. Please use a different one.', 'danger')
            else:
                user = User(
                    username=form.username.data, 
                    email=form.email.data, 
                    balance=form.balance.data, 
                    is_admin=form.is_admin.data
                )
                user.set_password(form.password.data)
                try:
                    db.session.add(user)
                    db.session.commit()
                    flash('User created successfully.', 'success')
                    return redirect(url_for('admin.list_users'))
                except Exception as e:
                    db.session.rollback()
                    flash(f'Error: {str(e)}', 'danger')
        else:
            flash('Form validation failed. Please correct the errors and try again.', 'danger')
    
    return render_template('admin/create_user.html', form=form)

@admin_bp.route('/admin/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.shop'))
    
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user)
    form.submit.label.text = 'Update User'

    if request.method == 'POST':
        form.username.data = request.form.get('username')
        form.email.data = request.form.get('email')
        form.balance.data = request.form.get('balance')
        form.is_admin.data = 'is_admin' in request.form
        form.password.data = request.form.get('password')
        form.confirm.data = request.form.get('confirm')

        if not form.username.data or not form.email.data or not form.balance.data:
            flash('Form validation failed. All fields are required.', 'danger')
        else:
            user.username = form.username.data
            user.email = form.email.data
            user.balance = form.balance.data
            user.is_admin = form.is_admin.data
            if form.password.data:
                if form.password.data == form.confirm.data:
                    user.set_password(form.password.data)
                else:
                    flash('Passwords do not match.', 'danger')
                    return render_template('admin/update_user.html', form=form, user_id=user_id)
            db.session.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('admin.list_users'))

    return render_template('admin/update_user.html', form=form, user_id=user_id)


@admin_bp.route('/admin/users')
@login_required
def list_users():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    users = User.query.all()
    return render_template('admin/list_users.html', users=users)

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
    return redirect(url_for('admin.list_users'))