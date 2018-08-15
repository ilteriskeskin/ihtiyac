from flask import Flask, render_template, flash, redirect, request, session, logging, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

# Kullanıcı Giriş Decorator'ı

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Bu sayfayı görüntülemek için lütfen giriş yapın.', 'danger')
            return redirect(url_for('login'))
    return decorated_function

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

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/need/<string:id>')
def need(id):
    need = Need.query.filter_by(id=id).first()
    return render_template('need.html', need = need)

@app.route('/dashboard')
@login_required
def dashboard():
    email = session['email']
    needs = Need.query.filter_by(email=email)
    if session['logged_in']:
        return render_template('dashboard.html', needs = needs)
    else:
        return render_template('dashboard.html')

@app.route('/needs')
def needs():
    needs = Need.query.all()
    if needs:
        return render_template('needs.html', needs = needs)
    else:
        return render_template('needs.html')
# İhtiyaç Ekleme

@app.route('/addneed', methods=['GET', 'POST'])
@login_required
def addneed():
    form = NeedForm(request.form)
    if request.method == 'POST' and form.validate():
        new_need = Need(title = form.title.data, content = form.content.data, 
                        address = form.address.data, email = form.email.data, 
                        phone = form.phone.data, category = form.category.data, 
                        iban = form.iban.data)

        db.session.add(new_need)
        db.session.commit()
        flash('Başarılı bir şekilde ihtiyaç eklediniz :)', 'success')
        
        return redirect(url_for('dashboard'))
    return render_template('addneed.html', form = form)

# Giriş Yapma

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate:
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                flash("Başarıyla Giriş Yaptınız", "success")
                
                session['logged_in'] = True
                session['email'] = user.email 

                return redirect(url_for('home'))
            else:
                flash("Kullanıcı Adı veya Parola Yanlış", "danger")
                return redirect(url_for('login'))

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
        flash('Başarılı bir şekilde kayıt oldunuz', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', form = form)

# Çıkış Yapma

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# İhtiyaç silme

@app.route('/delete/<string:id>')
@login_required
def delete(id):
    need = Need.query.filter_by(id = id).first()
    db.session.delete(need)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
