# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, FileField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')

class BlockForm(FlaskForm):
    title = StringField('Заголовок (UA)', validators=[DataRequired()])
    title_en = StringField('Заголовок (EN)', validators=[Optional()])
    title_de = StringField('Заголовок (DE)', validators=[Optional()])
    title_ru = StringField('Заголовок (RU)', validators=[Optional()])
    content = TextAreaField('Текст (UA)', validators=[Optional()])
    content_en = TextAreaField('Текст (EN)', validators=[Optional()])
    content_de = TextAreaField('Текст (DE)', validators=[Optional()])
    content_ru = TextAreaField('Текст (RU)', validators=[Optional()])
    image = FileField('Зображення', validators=[Optional()])
    is_active = BooleanField('Активний')
    is_top = BooleanField('Головний блок')
    submit = SubmitField('Зберегти')

class PaymentMethodForm(FlaskForm):
    name = StringField('Назва (UA)', validators=[DataRequired()])
    name_en = StringField('Назва (EN)', validators=[Optional()])
    name_de = StringField('Назва (DE)', validators=[Optional()])
    name_ru = StringField('Назва (RU)', validators=[Optional()])
    type = SelectField('Тип', choices=[('stripe', 'Stripe'), ('paypal', 'PayPal'), ('bank', 'Банк/QR'), ('custom', 'Інший')])
    details = TextAreaField('Реквізити (JSON)', validators=[Optional()])
    qr_code = FileField('QR-код', validators=[Optional()])
    description_ua = TextAreaField('Опис (UA)', validators=[Optional()])
    description_en = TextAreaField('Опис (EN)', validators=[Optional()])
    description_de = TextAreaField('Опис (DE)', validators=[Optional()])
    description_ru = TextAreaField('Опис (RU)', validators=[Optional()])
    is_active = BooleanField('Активний')
    submit = SubmitField('Зберегти')

class SettingsForm(FlaskForm):
    facebook = StringField('Facebook', validators=[Optional()])
    instagram = StringField('Instagram', validators=[Optional()])
    telegram = StringField('Telegram', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Зберегти')
