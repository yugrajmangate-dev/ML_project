from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    # Target linked Customer ID from dataset (e.g. '17850')
    customer_id = db.Column(db.String(50), nullable=True) 

class Product(db.Model):
    __tablename__ = 'product'
    # pandas to_sql respects the dataframe naming
    StockCode = db.Column(db.String(100), primary_key=True) 
    Description = db.Column(db.String(255), nullable=True)

class Interaction(db.Model):
    __tablename__ = 'interaction'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    stock_code = db.Column(db.String(100), db.ForeignKey('product.StockCode'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
