#models.py
from CompanyWebApp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

# USER LOADER: The user_loader decorator allows flask-login to load the current user and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#USER TABLE
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id =db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(100), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique = True, index=True)
    username = db.Column(db.String(64), unique = True, index=True)
    user_dep = db.Column(db.String(20), default='外部')
    user_level = db.Column(db.String(20), default='普通用户')
    admin = db.Column(db.Boolean,default=False)
    password_hash = db.Column(db.String(128))

    #ADD RELATIONSHIPS
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, user_dep, user_level, admin, password):
        self.email = email
        self.username = username
        self.user_dep = user_dep
        self.user_level = user_level
        self.admin = admin
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"username:{self.username}"

#BLOGPOSTS TABLE
class BlogPost(db.Model):
    
    __tablename__='blogposts'

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False) 
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    title = db.Column(db.String(140), nullable = False)
    text = db.Column(db.Text, nullable = False)
    
    users = db.relationship(User)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date}"

#TRADE TABLE
class Trade(db.Model):
    __tablename__ = 'trades'

    id = db.Column(db.Integer, primary_key = True)
    equip_amount = db.Column(db.Integer)
    rent_period = db.Column(db.Integer)
    downpayment = db.Column(db.Integer)
    deposit = db.Column(db.Integer)
    fee = db.Column(db.Integer)
    flat_rate = db.Column(db.Float)
    payment_type = db.Column(db.Text)
    payment_period = db.Column(db.Text)
    irr_nor = db.Column(db.Float)
    irr_exp = db.Column(db.Float)
    # one transaction to many cashflows
    cashflows = db.relationship('CashFlow', backref = 'trade', lazy = 'dynamic')

    def __init__(self, equip_amount,rent_period,downpayment,deposit,fee,flat_rate,payment_type,payment_period,irr_nor,irr_exp):
        self.equip_amount = equip_amount
        self.rent_period = rent_period
        self.downpayment = downpayment
        self.deposit = deposit
        self.fee = fee
        self.flat_rate = flat_rate
        self.payment_type = payment_type
        self.payment_period = payment_period
        self.irr_nor = irr_nor
        self.irr_exp = irr_exp
    
    def __repr__(self):
        if self.irr_nor and self.irr_nor:
            return f"代号{self.id},设备金额为{self.equip_amount}元的交易，IRR测算为{self.irr_nor}%/年，连续复利IRR测算为{self.irr_exp}%/年"
        else:
            return f"代号{self.id},设备金额为{self.equip_amount}元的交易, 请测算IRR"

    def report_cashflows(self):
        print(f"here are the cashflows of the trade {self.id}")
        for cashflow in self.cashflows:
            print(cashflow.cashflow_amount)

#CASHFLOWS TABLE
class CashFlow(db.Model):
    __tablename__ = 'cashflows'

    id = db.Column(db.Integer, primary_key = True)
    tra_id = db.Column(db.Integer, db.ForeignKey('trades.id'))
    date = db.Column(db.Date)
    cashflow_nature = db.Column(db.String(64))
    cashflow_type = db.Column(db.Integer)
    cashflow_amount = db.Column(db.Integer)
    cashflow_tax = db.Column(db.Integer)

    def __init__(self, tra_id, date, cashflow_nature, cashflow_type,cashflow_amount,cashflow_tax):
        self.tra_id = tra_id
        self.date = date
        self.cashflow_nature = cashflow_nature
        self.cashflow_type = cashflow_type
        self.cashflow_amount = cashflow_amount
        self.cashflow_tax = cashflow_tax

    def __repr__(self):
        return f"交易代码{self.tra_id}，日期{self.date}，性质{self.cashflow_nature}，金额{self.cashflow_amount}"