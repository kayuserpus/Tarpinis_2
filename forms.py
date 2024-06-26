from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from app import db
import re

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
            raise ValidationError('Please use a different email address.')

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

class ItemForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Product')

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Product')

class DiscountForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    discount_percentage = FloatField('Discount Percentage', validators=[DataRequired()])
    submit = SubmitField('Set Discount')
