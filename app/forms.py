# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, BooleanField, FileField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Optional

class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')

class BlockForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[Optional()])
    image = FileField('Зображення', validators=[Optional()])
    is_active = BooleanField('Активний')
    is_top = BooleanField('Головний блок')
    submit = SubmitField('Зберегти')

class PaymentMethodForm(FlaskForm):
    name = StringField('Назва', validators=[DataRequired()])
    type = SelectField('Тип', choices=[('stripe', 'Stripe'), ('paypal', 'PayPal'), ('bank', 'Банк/QR'), ('custom', 'Інший')])
    details = TextAreaField('Реквізити (JSON)', validators=[Optional()])
    qr_code = FileField('QR-код', validators=[Optional()])
    description_ua = TextAreaField('Опис (UA)', validators=[Optional()])
    description_en = TextAreaField('Опис (EN)', validators=[Optional()])
    description_ru = TextAreaField('Опис (RU)', validators=[Optional()])
    is_active = BooleanField('Активний')
    submit = SubmitField('Зберегти')

class SettingsForm(FlaskForm):
    facebook = StringField('Facebook', validators=[Optional()])
    instagram = StringField('Instagram', validators=[Optional()])
    telegram = StringField('Telegram', validators=[Optional()])
    email = StringField('Email', validators=[Optional(), Email()])
    submit = SubmitField('Зберегти')
