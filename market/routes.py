from operator import methodcaller
from os import SEEK_CUR
import re

from flask_wtf import form
from sqlalchemy.orm.query import QueryContext
from market import app, db
from market.models import Item, User
from flask import render_template, redirect, url_for, flash, request
from market.forms import AddItem, DeleteItemForm, FundsForm, RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user
from market.Controllers import logoutController, loginController, mailController

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('Home.html')

@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchaseForm = PurchaseItemForm()
    sellForm = SellItemForm()
    deleteForm = DeleteItemForm()

    if request.method == 'POST':
        purchasedItem = request.form.get('purchased_item')
        pItemObj = Item.query.filter_by(name=purchasedItem).first()
        #buy logic
        if pItemObj:
            if current_user.canPurchase(pItemObj):
                pItemObj.buy(current_user)

                mail = mailController.Email(app)
                mail.sendMail(current_user.username)
                #msg = Message('Hello', sender = 'yourId@gmail.com', recipients = ['someone1@gmail.com'])
                #msg.body = "This is the email body"
                #mail.send(msg)

                flash(f"Congratulations you purchase: {pItemObj.name} for ${pItemObj.price}", category='success')
            else:
                flash(f"Not enough funds.", category='danger')
        #sell logic
        soldItem = request.form.get('sold_item')
        sItemObj = Item.query.filter_by(name=soldItem).first()
        if soldItem:
            if current_user.canSell(sItemObj):
                sItemObj.sell(current_user)
                flash(f"Congratulations you sold: {sItemObj.name} for ${sItemObj.price}", category='success')
            else:
                flash(f"Something went wrong with selling {sItemObj.name}.", category='danger')

        #delete logic
        deleteItem = request.form.get('delete_item')
        dDeleteItem = Item.query.filter_by(name=deleteItem).first()
        if deleteItem:
            db.session.delete(dDeleteItem)
            db.session.commit()
        return redirect(url_for('market_page'))    
    
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        ownedItems = Item.query.filter_by(owner=current_user.id)
        return render_template('Market.html', items=items, columns=Item.columns(), purchaseForm = purchaseForm, owned=ownedItems, sellForm=sellForm, deleteForm=deleteForm)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                            email_address=form.email.data,
                            #use the setter created not password_hash itself
                            password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created! You are now logged in as: {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    isRedirect = loginController.login()
    #form = LoginForm()
    #if form.validate_on_submit():
    #    attempted_user = User.query.filter_by(username=form.username.data).first()
    #    if attempted_user and attempted_user.check_password_correction(form.password.data):
    #        login_user(attempted_user)
    #        flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
    #        return redirect(url_for('market_page'))
    #    else:
    #        flash(f'Username and password are not match! Please try again.', category='danger')
    if isRedirect:
        return redirect(url_for('market_page'))
    return render_template('login.html', form=LoginForm())

@app.route('/logout')
def logout_page():  
    logoutController.logout()
    #logout_user()
    #flash(f'You have logged out', category='info')
    return redirect(url_for('home_page'))

@app.route('/about/<username>')
def about(username):
    return f'<h1>ABOUT SECTION for {username}</h1>'

@app.route('/add', methods=['GET','POST'])
def addItem():
    form = AddItem()
    if form.validate_on_submit():
        #to create an instance of the model, the proper way is to set in the parameters the properties to the data
        # <<property>> = form.<<property>>.data
        item_to_create= Item(name=form.name.data,
                            price=form.price.data,
                            barcode=form.barcode.data,
                            description=form.description.data,
                            owner = current_user.id
                            )
        db.session.add(item_to_create)
        db.session.commit()


        return redirect(url_for('market_page'))
    return render_template('addItem.html', form=form)

@app.route('/funds/<username>', methods=['GET', 'POST'])
def funds_page(username):
    form = FundsForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user:
            user.addFunds(form.amount.data)
            flash(f'The amount of {form.amount.data} was succesfully added', category='success')
            return redirect(url_for('home_page'))

    return render_template('addFunds.html', form=form)