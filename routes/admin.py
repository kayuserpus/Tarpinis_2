from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models import Item, Discount
from forms import ItemForm, DiscountForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    return render_template('admin/admin.html')

@admin_bp.route('/admin/add_Item', methods=['GET', 'POST'])
@login_required
def add_Item():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    form = ItemForm()
    if form.validate_on_submit():
        Item = Item(name=form.name.data, price=form.price.data, quantity=form.quantity.data, description=form.description.data)
        db.session.add(Item)
        db.session.commit()
        flash('Item added successfully.')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_Item.html', form=form)

@admin_bp.route('/admin/set_discount', methods=['GET', 'POST'])
@login_required
def set_discount():
    if not current_user.is_admin:
        flash('Admin access required.')
        return redirect(url_for('user.shop'))
    form = DiscountForm()
    if form.validate_on_submit():
        Item = Item.query.get(form.Item_id.data)
        if Item:
            discount = Discount(Item_id=Item.id, discount_percentage=form.discount_percentage.data)
            db.session.add(discount)
            db.session.commit()
            flash('Discount set successfully.')
        else:
            flash('Item not found.')
    return render_template('admin/set_discount.html', form=form)
