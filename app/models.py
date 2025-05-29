# app/models.py

from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """Адміністратор сайту"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

class Block(db.Model):
    """Контентний блок (для 6 секцій сайту)"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    content = db.Column(db.Text)
    image = db.Column(db.String(256))
    order = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)
    slug = db.Column(db.String(64), unique=True)
    is_top = db.Column(db.Boolean, default=False)  # Нове поле: головний блок

class PaymentMethod(db.Model):
    """Метод оплати (Stripe, PayPal, N26, QR, тощо)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.String(32))
    details = db.Column(db.JSON)
    qr_code = db.Column(db.String(256))
    description_ua = db.Column(db.Text)
    description_en = db.Column(db.Text)
    description_ru = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=1)
    invoice_pdf = db.Column(db.String(256))

class Payment(db.Model):
    """Історія/заявки оплат з сайту"""
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    amount = db.Column(db.Float)
    method_id = db.Column(db.Integer, db.ForeignKey('payment_method.id'))
    status = db.Column(db.String(32), default='pending') # pending/paid/failed
    payment_info = db.Column(db.JSON)
    invoice_pdf = db.Column(db.String(256))
    proof_image = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    method = db.relationship('PaymentMethod')

class Settings(db.Model):
    """Налаштування сайту"""
    id = db.Column(db.Integer, primary_key=True)
    facebook = db.Column(db.String(256))
    instagram = db.Column(db.String(256))
    telegram = db.Column(db.String(256))
    email = db.Column(db.String(256))
