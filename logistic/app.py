from flask import Flask,flash, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, Integer
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a989e8c0679101b2fa3f510eea014e41'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user='postgres',
    pw='1234',
    url='localhost:5433',
    db='logistic'
)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(50), nullable=True)
    town_name = db.Column(db.String(50), nullable=True)
    district_name = db.Column(db.String(50), nullable=True)
    apartment_no = db.Column(db.Integer)

class branch(db.Model):
    branch_id = db.Column(db.Integer, primary_key=True)
    branch_name = db.Column(db.String(100), nullable=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    capacity = db.Column(db.Integer)

class product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float)
    expiration_date = db.Column(db.Date)
    kdv = db.Column(db.Integer)

class beverage(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float)
    expiration_date = db.Column(db.Date)
    kdv = db.Column(db.Integer)
    quantity_lt = db.Column(db.Float)

class butcher(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float)
    expiration_date = db.Column(db.Date)
    kdv = db.Column(db.Integer)
    quantity_kg = db.Column(db.Float)

class cleaning(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=True)
    price = db.Column(db.Float)
    expiration_date = db.Column(db.Date)
    kdv = db.Column(db.Integer)
    clean_type = db.Column(db.String(100), nullable=True)

class container(db.Model):
    container_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    weight = db.Column(db.Float)

class store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    store_name = db.Column(db.String(100), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    product_quantity = db.Column(db.Integer)

class vehicle(db.Model):
    vehicle_id = db.Column(db.Integer, primary_key=True)
    plate = db.Column(db.String(100), nullable=True)
    chassis_no = db.Column(db.String(100), nullable=True)
    container_id = db.Column(db.Integer, db.ForeignKey('container.container_id'), nullable=False)

class delivery(db.Model):
    delivery_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)

class driver(db.Model):
    driver_id = db.Column(db.Integer, primary_key=True)
    driver_name = db.Column(db.String(100), nullable=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.vehicle_id'), nullable=False)
    driver_licence = db.Column(db.String(100), nullable=True)

class personal(db.Model):
    ssn = db.Column(db.Integer, primary_key=True)
    personal_name = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(100), nullable=True)

class manager(db.Model):
    ssn = db.Column(db.Integer, primary_key=True)
    personal_name = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(100), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)

class sales_consultant(db.Model):
    ssn = db.Column(db.Integer, primary_key=True)
    personal_name = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(100), nullable=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)

class store_personal(db.Model):
    ssn = db.Column(db.Integer, primary_key=True)
    personal_name = db.Column(db.String(100), nullable=True)
    job_title = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(100), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)

class product_demand(db.Model):
    demand_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    product_quantity = db.Column(db.Integer)
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.branch_id'), nullable=False)
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(180))
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route("/")
def index():
    return render_template("index.html",title="Hosgeldiniz")

'''
    burasi person listelenmesi için kullanilacak
    content array olacak buna gore frontend de basilacak
'''
@app.route("/person/list", methods = ['POST', 'GET'])
def personList():
    data = personal.query.all()
    return render_template("personList.html", content=data,title="Personel Liste")

@app.route("/person/add", methods = ['POST', 'GET'])
def person():
    if request.method == 'POST':
        data = request.form
        person = personal(
            ssn=data.get('ssn'),
            personal_name=data.get('personal_name'),
            job_title=data.get('job_title'),
            email=data.get('email'),
            phone_number=data.get('phone_number')
        )
        db.session.add(person)
        db.session.commit()
        flash('Personel eklendi')
        return render_template("person.html", title="Personel Yonetim")
    return render_template("person.html",title="Personel Yonetim")

@app.route("/person/update", methods = ['POST', 'GET'])
def person_update():
    personals = personal.query.all()
    ssn = [item.ssn for item in personals]
    if request.method == 'POST':
        data = request.form
        getssn = data.get('getssn')
        data_dict = dict((key, request.form.get(key)) for key in data.keys())
        data_dict.pop('getssn')
        for k in data.keys():
            if data_dict.get(k) == '':
                data_dict.pop(k)
        personal.query.filter_by(ssn=str(getssn)).update(data_dict)
        db.session.commit()
        return render_template("person_update.html")
    return render_template("person_update.html", personal_list=ssn,title="Personel Guncelleme")

'''
buradaki dashboad methodu personel ekleme ve personel yonetiminde kullanilacaktir 
'''
@app.route("/personel", methods = ['POST', 'GET'])
def dashboard():
    return render_template("dashboard.html",title="Personel Yonetim")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    
    
    
    

'''
depolarin listelenmesinde ullanilacak olan method
'''
@app.route("/depo/list", methods = ['POST', 'GET'])
def depotList():
    branches = branch.query.add_columns(branch.address_id,branch.branch_id,branch.branch_name,branch.capacity,address.address_id,address.apartment_no,address.country_name,address.district_name,address.town_name).filter(branch.address_id == address.address_id)
    #branches = branch.query.join(address, branch.address_id == address.address_id)
    return render_template("depo.html", content=branches, title="Depo listesi")

'''
depolarin yonetiminde kullanilacak sayfa
'''
@app.route("/depo/arrange", methods = ['POST', 'GET'])
def depot_arrangnment():
    depos = store.query.all()
    store_ids = [item.store_id for item in depos]
    if request.method == 'POST':
        data = request.form
        store_id = data.get('get_store_id')
        data_dict = dict((key, request.form.get(key)) for key in data.keys())
        data_dict.pop('get_store_id')
        for k in data.keys():
            if data_dict.get(k) == '':
                data_dict.pop(k)
        store.query.filter_by(store_id=str(store_id)).update(data_dict)
        db.session.commit()
        return render_template("store_update.html")
    return render_template("store_update.html", store_list=store_ids)

@app.route("/product/add", methods = ['POST', 'GET'])
def product_add():
    if request.method == 'POST':
        data = request.form
        try:
            # eğer ürün miktar içeriyorsa butcher yada beverage ürününe eklenecek
            int(data.get("quantity")) / 1
            if data.get('getproduct') == 'beverage':
                product = beverage(
                    product_id = data.get('product_id'),
                    product_name = data.get('product_name'),
                    price = float(data.get('price')),
                    expiration_date = data.get('expiration_date'),
                    kdv = float(data.get('kdv')),
                    quantity_lt = float(data.get('quantity'))
                )
            if data.get('getproduct') == 'butcher':
                product = butcher(
                    product_id=data.get('product_id'),
                    product_name=data.get('product_name'),
                    price=float(data.get('price')),
                    expiration_date=data.get('expiration_date'),
                    kdv=float(data.get('kdv')),
                    quantity_kg=float(data.get('quantity'))
                )
        except:
            product = cleaning(
                product_id=data.get('product_id'),
                product_name=data.get('product_name'),
                price=float(data.get('price')),
                expiration_date=data.get('expiration_date'),
                kdv=float(data.get('kdv')),
                clean_type=data.get('quantity')
            )
        db.session.add(product)
        db.session.commit()
        flash('Urun eklendi')
    return render_template("product.html", product_list = ['beverage', 'butcher', 'cleaning'],title="Urun Ekleme")

@app.route("/delivery/list")
def delivery_list():
    content = delivery.query.add_columns(
        delivery.delivery_id,
        store.store_name,
        branch.branch_name,
        vehicle.plate
    ).filter(
        delivery.store_id==store.store_id
    ).filter(
        delivery.branch_id==branch.branch_id
    ).filter(
        delivery.vehicle_id==vehicle.vehicle_id
    )
    for c in content:
        print(c)
    return render_template("delivery.html", content=content)

@app.route("/delivery/add", methods = ['POST', 'GET'])
def delivery_add():
    if request.method == 'POST':
        data = request.form
        mov = delivery(
            delivery_id=data.get("delivery_id"),
            store_id=data.get("store_id"),
            branch_id=data.get("branch_id"),
            vehicle_id=data.get("vehicle_id")
        )
        db.session.add(mov)
        db.session.commit()
        flash('Urun eklendi')
    return render_template("delivery_add.html")

if __name__=='__main__':
    app.run(debug=True)