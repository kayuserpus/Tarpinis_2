from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, NumberRange, Optional
from app.models import User, Product 
from app import db
import re

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    balance = DecimalField('Balance', validators=[Optional(), NumberRange(min=0, message="Balance must be 0 or more")])
    is_admin = BooleanField('Is Admin')
    password = PasswordField('Password')
    confirm = PasswordField('Repeat Password', validators=[EqualTo('password', message="Passwords must match")])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        if kwargs.get('update'):
            self.password.render_kw = {"placeholder": "Leave empty if not changing"}
            self.confirm.render_kw = {"placeholder": "Leave empty if not changing"}

    def validate_email(self, email):
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email.data):
            raise ValidationError('Invalid email format. Must be in the format name@domain.com.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already in use. Please use a different email address.')
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email.data):
            raise ValidationError('Invalid email format. Must be in the format name@domain.com.')

    def validate_password(self, password):
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password.data):
            raise ValidationError('Password must be at least 8 characters long, include letters and numbers.')

    def save_user(self):
        user = User(username=self.username.data, email=self.email.data)
        user.set_password(self.password.data)
        db.session.add(user)
        db.session.commit()
        return user

class BalanceForm(FlaskForm):
    amount = DecimalField('Amount', validators=[DataRequired(), NumberRange(min=0, message="Amount must be positive")])
    submit = SubmitField('Submit')

class CartForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add to Cart')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = TextAreaField('Description')
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Add Product')

    def validate_price(form, field):
        if field.data < 0:
            raise ValidationError('Price must be non-negative.')

    def validate_quantity(form, field):
        if field.data < 0:
            raise ValidationError('Quantity must be non-negative.')

class DiscountForm(FlaskForm):
    product_id = SelectField('Product', choices=[], coerce=int, validators=[DataRequired()])
    discount_percentage = FloatField('Discount Percentage', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Set Discount')

    def __init__(self, *args, **kwargs):
        super(DiscountForm, self).__init__(*args, **kwargs)
        self.product_id.choices = [(product.id, product.name) for product in Product.query.all()]
