from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Float, Integer

app = Flask(__name__)

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


# db yaratmak için
# createdb -h localhost -p 5432 -U <username> <dbname>
# postgresql bağlanmak için
# psql -h localhost -p 5432 -d postgres

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/person/list", methods = ['POST', 'GET'])
def personList():
    data = personal.query.all()
    return render_template("personList.html", content=data)

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
    return render_template("person_update.html", personal_list=ssn)

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
        return render_template("person.html", title="Personel Yonetim")
    return render_template("person.html",title="Personel Yonetim")

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
    return render_template("product.html", product_list = ['beverage', 'butcher', 'cleaning'])

@app.route("/product/list", methods = ['POST', 'GET'])
def product_list():
    if request.method == 'POST':
        data = request.form
        type = data.get('getproduct')
        if type == 'beverage':
            content = beverage.query.all()
        elif type == 'butcher':
            content = butcher.query.all()
        else:
            content = cleaning.query.all()
        return render_template("product_list.html", content = content)
    return render_template("product_list.html", product_list = ['beverage', 'butcher', 'cleaning'])

'''
buradaki dashboad methodu personel ekleme ve personel yonetiminde kullanilacaktir 
'''
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",title="dashboard")

@app.route("/login")
def login():
    return render_template("login.html",title="Login")

@app.route("/signup")
def signup():
    return render_template("signup.html",title="Sign up")

'''
depolarin listelenmesinde ullanilacak olan method
'''
@app.route("/depo/list")
def depotList():
    branches = branch.query.join(address, branch.address_id == address.address_id)
    return render_template("depo.html", content=branches, title="Depo listesi")

'''
depolarin yonetiminde kullanilacak sayfa
'''
@app.route("/depo/arrange")
def depotArrangnment():
    return render_template("depoArrangment.html",title="Depo listesi")



if __name__=='__main__':
    app.run(debug=True)