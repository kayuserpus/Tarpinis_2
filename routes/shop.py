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

