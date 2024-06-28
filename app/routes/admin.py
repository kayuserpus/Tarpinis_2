from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Product, Discount, User
from forms import ProductForm, DiscountForm, UserForm
import re

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
    
    if request.method == 'POST':
        if not form.validate():
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'Error in {fieldName}: {err}', 'danger')
        else:
            existing_product = Product.query.filter_by(name=form.name.data).first()
            if existing_product:
                flash('Product with this name already exists. Please choose a different name.', 'danger')
            else:
                try:
                    product = Product(
                        name=form.name.data,
                        price=form.price.data,
                        quantity=form.quantity.data,
                        description=form.description.data,
                        category=form.category.data
                    )
                    db.session.add(product)
                    db.session.commit()
                    flash('Product added successfully.')
                    return redirect(url_for('admin.admin_dashboard'))
                except Exception as e:
                    flash(f'An error occurred while adding the product: {str(e)}', 'danger')
    
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
    
    if request.method == 'POST':
        if not form.validate():
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'Error in {fieldName}: {err}', 'danger')
        else:
            try:
                product.quantity = form.quantity.data
                db.session.commit()
                flash('Product quantity updated successfully.', 'success')
                return redirect(url_for('admin.list_products'))
            except Exception as e:
                flash(f'An error occurred while updating the product quantity: {str(e)}', 'danger')
    
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
    
    if form.validate_on_submit():
        product_id = form.product_id.data
        discount_percentage = form.discount_percentage.data
        
        existing_discount = Discount.query.filter_by(product_id=product_id).first()
        if existing_discount:
            flash('This product already has a discount.', 'danger')
        else:
            try:
                discount = Discount(product_id=product_id, discount_percentage=discount_percentage)
                db.session.add(discount)
                db.session.commit()
                flash('Discount set successfully.', 'success')
                return redirect(url_for('admin.list_discounts'))
            except Exception as e:
                flash(f'An error occurred while setting the discount: {str(e)}', 'danger')
    
    return render_template('admin/set_discount.html', form=form)

@admin_bp.route('/admin/discounts')
@login_required
def list_discounts():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    discounts = Discount.query.all()
    products = {product.id: product.name for product in Product.query.all()}
    return render_template('admin/list_discounts.html', discounts=discounts, products=products)

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
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm_password = form.confirm.data

        errors = []

        if not username:
            errors.append('Username is required.')

        if not email:
            errors.append('Email is required.')
        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            errors.append('Invalid email format. Must be in the format name@domain.com.')

        if not password:
            errors.append('Password is required.')
        elif not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            errors.append('Password must be at least 8 characters long, include letters and numbers.')

        if password != confirm_password:
            errors.append('Passwords do not match.')

        if User.query.filter_by(username=username).first():
            errors.append('Username already taken. Please choose a different one.')

        if User.query.filter_by(email=email).first():
            errors.append('Email address already registered. Please use a different one.')

        if errors or not form.validate():
            for error in errors:
                flash(error, 'danger')
            for field, error_messages in form.errors.items():
                for error in error_messages:
                    flash(f"Error in {field}: {error}", 'danger')
            return render_template('admin/create_user.html', form=form)

        user = User(
            username=username, 
            email=email, 
            balance=form.balance.data, 
            is_admin=form.is_admin.data
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('User created successfully.', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
    
    return render_template('admin/create_user.html', form=form)

@admin_bp.route('/admin/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if not current_user.is_admin:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('user.shop'))
    
    user = User.query.get_or_404(user_id)
    form = UserForm(obj=user, update=True)
    form.submit.label.text = 'Update User'

    if request.method == 'POST':
        username = form.username.data
        email = form.email.data
        balance = form.balance.data
        is_admin = form.is_admin.data
        password = form.password.data

        errors = []

        if not username:
            errors.append('Username is required.')

        if not email:
            errors.append('Email is required.')
        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            errors.append('Invalid email format. Must be in the format name@domain.com.')

        existing_user_username = User.query.filter(User.user_id != user.user_id, User.username == username).first()
        existing_user_email = User.query.filter(User.user_id != user.user_id, User.email == email).first()

        if existing_user_username:
            errors.append('Username already taken. Please choose a different one.')
        if existing_user_email:
            errors.append('Email address already registered. Please use a different one.')

        if errors or not form.validate():
            for error in errors:
                flash(error, 'danger')
            for field, error_messages in form.errors.items():
                for error in error_messages:
                    flash(f"Error in {field}: {error}", 'danger')
            return render_template('admin/update_user.html', form=form, user_id=user_id)

        user.username = username
        user.email = email
        user.balance = balance
        user.is_admin = is_admin
        if password:
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
                flash('Password must be at least 8 characters long, include letters and numbers.', 'danger')
                return render_template('admin/update_user.html', form=form, user_id=user_id)
            user.set_password(password)
        try:
            db.session.commit()
            flash('User updated successfully.', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    
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
