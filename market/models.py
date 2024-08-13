from enum import unique
from sqlalchemy.orm import backref
from market import db, bcrypt, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email_address = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettyBudget(self):
        if len(str(self.budget)) >= 4:
            return f'${str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f"${self.budget}"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_pwd):
        self.password_hash = bcrypt.generate_password_hash(plain_text_pwd).decode('utf-8')

    def check_password_correction(self, attemped_password):
        return bcrypt.check_password_hash(self.password_hash, attemped_password)

    def canPurchase(self, itemObj):
        return self.budget >= itemObj.price

    def canSell(self, itemObj):
        return itemObj in self.items
    
    def purchase(self, item):
        item.owner = self.id
        self.budget -= item.price
        db.session.commit()
    
    def addFunds(self, amount):
        self.budget += amount
        db.session.commit()

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=True, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item {self.name}'
    
    def columns():
        return ['id', 'name', 'price', 'barcode']

    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()