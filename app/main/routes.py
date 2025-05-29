# app/main/routes.py

from flask import Blueprint, render_template, redirect, url_for, abort
from app.models import Block, PaymentMethod, Settings
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Головна сторінка з 6 блоками"""
    blocks = Block.query.filter_by(is_active=True).order_by(Block.order).all()
    methods = PaymentMethod.query.filter_by(is_active=True).order_by(PaymentMethod.order).all()
    settings = Settings.query.first()
    return render_template('index.html', blocks=blocks, methods=methods, settings=settings)

@main.route('/block/<slug>')
def block_detail(slug):
    """Детальна сторінка блоку"""
    block = Block.query.filter_by(slug=slug, is_active=True).first_or_404()
    return render_template('block_detail.html', block=block)

@main.route('/payment')
def payment():
    """Сторінка з усіма методами оплати"""
    methods = PaymentMethod.query.filter_by(is_active=True).order_by(PaymentMethod.order).all()
    return render_template('payment.html', methods=methods)

@main.route('/privacy')
def privacy():
    return render_template('privacy.html')

@main.route('/impressum')
def impressum():
    return render_template('impressum.html')

@main.route('/contacts')
def contacts():
    return render_template('contacts.html')
