from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

# Kullanıcı Veritabanı

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(25), unique=True)

# Kullanıcı İhtiyaç Veritabanı

class Need(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    address = db.Column(db.String(1000))
    email = db.Column(db.String(45))
    phone = db.Column(db.Integer)
    category = db.Column(db.String(40))
    iban = db.Column(db.String(50))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
