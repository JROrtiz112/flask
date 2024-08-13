import re
from flask import redirect, url_for, flash
from flask_login import login_user
from market.forms import LoginForm
from market.models import User

def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return True
            #redirect(url_for('market_page'))
        else:
            flash(f'Username and password are not match! Please try again.', category='danger')
            return False
    return False