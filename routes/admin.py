from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, Discount
from forms import ProductForm, DiscountForm

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
