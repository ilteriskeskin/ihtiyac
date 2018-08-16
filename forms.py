from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import DataRequired

# İhtiyaç Formu

class NeedForm(Form):
    title = StringField('Başlık', validators=[validators.Length(min=5, max=100), validators.DataRequired(message='Lütfen Bu Alanı Doldurun')])
    content = TextAreaField('İçerik', validators=[validators.Length(min=20, max=1000), validators.DataRequired(message='Lütfen Bu Alanı Doldurun')])
    address = TextAreaField('Adres', validators=[validators.Length(min=15, max=1000), validators.DataRequired(message=('Lütfen Bu Alanı Doldurun'))])
    email = StringField('Email', validators=[validators.Email(message='Lütfen Geçerli Bir Email Adresi Girin')])
    phone = IntegerField('Telefon', validators=[validators.DataRequired(message='Lütfen Bu Alanı Doldurun')])
    category = StringField('Kategori', validators=[validators.Length(min=5, max=50), validators.DataRequired(message='Lütfen Bu Alanı Doldurun')])
    iban = StringField('IBAN', validators=[validators.DataRequired(message='Lütfen Bu Alanı Doldurun')])

# Kullanıcı giriş formu

class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    password = PasswordField("Parola", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])

# Kullanıcı kayıt formu

class RegisterForm(Form):
    name = StringField("Ad", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    email = StringField("Email", validators=[validators.Email(message="Lütfen Geçerli Bir Email Adresi Girin")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen Bu Alanı Doldurun"),
        validators.EqualTo(fieldname="confirm", message="Parolalarınız Uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
