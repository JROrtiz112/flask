from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('This username is already being used!')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email_address=email_to_check.data).first()
        if email:
            raise ValidationError('This email is already being used!')

    username = StringField(label='User name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email:', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create account')

class LoginForm(FlaskForm):
    username = StringField(label='User name:', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')

class DeleteItemForm(FlaskForm):
    submit = SubmitField(label='Delete Item')

class AddItem(FlaskForm):
    name = StringField(label='Name', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    barcode = IntegerField(label='Barcode', validators=[DataRequired()])
    description = StringField(label='Description', validators=[DataRequired()])
    submit = SubmitField(label='Insert Item')

class FundsForm(FlaskForm):
    amount = IntegerField(label='Amount', validators=[DataRequired()])
    submit = SubmitField(label='Add funds')