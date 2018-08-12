from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linuxdegilgnulinux'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ilteriskeskin/Çalışma/ihtiyac/data.db'
db = SQLAlchemy(app)

# Kullanıcı Veritabanı

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(15), unique=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(25), unique=True)

# Kullanıcı giriş formu

class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    password = PasswordField("Parola", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])

# Kullanıcı kayıt formu

class RegisterForm(Form):
    name = StringField("Ad", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=3, max=25), validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])
    email = StringField("Email", validators=[validators.Email(message="Lütfen Geçerli Bir Email Adresi Giriniz")])
    password = PasswordField("Parola", validators=[
        validators.DataRequired(message="Lütfen Bu Alanı Doldurun"),
        validators.EqualTo(fieldname="confirm", message="Parolalarınız Uyuşmuyor")
    ])
    confirm = PasswordField("Parola Doğrula", validators=[validators.DataRequired(message="Lütfen Bu Alanı Doldurun")])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/grants/<string:id>')
def detail(id):
    return 'Help ID: ' + id

# Giriş Yapma

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('home'))

    return render_template('login.html', form = form)

# Kayıt Olma

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name = form.name.data, username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template('register.html', form = form)

# Çıkış Yapma

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
