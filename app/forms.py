from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, BooleanField, FileField,
    FloatField, SelectField, SubmitField
)
from wtforms.validators import DataRequired, Email, Optional, Length

class LoginForm(FlaskForm):
    username = StringField('Логін', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(max=128)])
    submit = SubmitField('Увійти')

class BlockForm(FlaskForm):
    title = StringField('Заголовок (UA)', validators=[DataRequired(), Length(max=120)])
    title_en = StringField('Заголовок (EN)', validators=[Optional(), Length(max=120)])
    title_de = StringField('Заголовок (DE)', validators=[Optional(), Length(max=120)])
    title_ru = StringField('Заголовок (RU)', validators=[Optional(), Length(max=120)])
    
    content = TextAreaField('Текст (UA)', validators=[Optional(), Length(max=4000)])
    content_en = TextAreaField('Текст (EN)', validators=[Optional(), Length(max=4000)])
    content_de = TextAreaField('Текст (DE)', validators=[Optional(), Length(max=4000)])
    content_ru = TextAreaField('Текст (RU)', validators=[Optional(), Length(max=4000)])
    
    image = FileField('Зображення', validators=[Optional()])
    is_active = BooleanField('Активний')
    is_top = BooleanField('Головний блок')
    submit = SubmitField('Зберегти')

class PaymentMethodForm(FlaskForm):
    name = StringField('Назва (UA)', validators=[DataRequired(), Length(max=120)])
    name_en = StringField('Назва (EN)', validators=[Optional(), Length(max=120)])
    name_de = StringField('Назва (DE)', validators=[Optional(), Length(max=120)])
    name_ru = StringField('Назва (RU)', validators=[Optional(), Length(max=120)])
    type = SelectField('Тип', choices=[
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('bank', 'Банк/QR'),
        ('custom', 'Інший')
    ])
    details = TextAreaField('Реквізити (JSON)', validators=[Optional(), Length(max=2000)])
    qr_code = FileField('QR-код', validators=[Optional()])
    description_ua = TextAreaField('Опис (UA)', validators=[Optional(), Length(max=2000)])
    description_en = TextAreaField('Опис (EN)', validators=[Optional(), Length(max=2000)])
    description_de = TextAreaField('Опис (DE)', validators=[Optional(), Length(max=2000)])
    description_ru = TextAreaField('Опис (RU)', validators=[Optional(), Length(max=2000)])
    is_active = BooleanField('Активний')
    submit = SubmitField('Зберегти')

class SettingsForm(FlaskForm):
    facebook = StringField('Facebook', validators=[Optional(), Length(max=120)])
    instagram = StringField('Instagram', validators=[Optional(), Length(max=120)])
    telegram = StringField('Telegram', validators=[Optional(), Length(max=120)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField('Зберегти')
