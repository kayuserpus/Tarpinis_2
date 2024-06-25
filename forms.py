from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from models import User  # Import correctly

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

class BalanceForm(FlaskForm):
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add to Balance')

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

class DiscountForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    discount_percentage = FloatField('Discount Percentage', validators=[DataRequired()])
    submit = SubmitField('Set Discount')
