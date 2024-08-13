from flask import redirect, url_for, flash
from flask_login import logout_user


def logout():
    logout_user()
    flash(f'You have logged out', category='info')
    return redirect(url_for('home_page'))