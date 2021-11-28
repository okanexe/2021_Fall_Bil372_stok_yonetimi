from flask import Flask,flash, render_template, request,redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, Integer
import psycopg2 
import psycopg2.extras
import re 
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a989e8c0679101b2fa3f510eea014e41'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user='okans',
    pw='',
    url='localhost:5432',
    db='logistic'
)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)


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
    
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)


@app.route("/")
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
    
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get('username')  
        password = request.form.get('password')
        print(password)
 
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')
 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
    
        _hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            cursor.execute("INSERT INTO users (fullname, username, password, email) VALUES (%s,%s,%s,%s)", (fullname, username, _hashed_password, email))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

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