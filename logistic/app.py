from flask import Flask, render_template, request
import psycopg2
from flask_sqlalchemy import SQLAlchemy

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
    #user = User.query.filter_by(username="elifcan").first()
    result = db.engine.execute("select * from personal")
    data = [row[0] for row in result]
    print(data)
    return render_template("index.html")

@app.route("/adress")
def fetch():
    conn = psycopg2.connect("dbname=guru99 user=okans password=")
    cur = conn.cursor()

    try:
        cur.execute('select * from address')
    except:
        conn.rollback()
    else:
        conn.commit()

    data = cur.fetchall()
    return "<p>{}</p>".format(data[0])


'''
    burasi person listelenmesi için kullanilacak
    content array olacak buna gore frontend de basilacak
'''
@app.route("/person/list", methods = ['POST', 'GET'])
def personList():
    conn = psycopg2.connect("dbname=guru99 user=okans password=")
    cur = conn.cursor()
    sql_command = "select * from personal"
    cur.execute(sql_command)
    data = cur.fetchall()
    return render_template("personList.html", content=data)

@app.route("/person/update", methods = ['POST', 'GET'])
def person_update():
    conn = psycopg2.connect("dbname=guru99 user=okans password=")
    cur = conn.cursor()
    cur.execute("select * from personal")
    ssn = [item[0] for item in cur.fetchall()]
    print(ssn)
    if request.method == 'POST':
        result = request.form
        print(result.keys())
        print(result.get('ssn'))
        for key in result.keys():
            if key == 'ssn':
                sql_command = "UPDATE personal SET ssn = %s where ssn = %s"
                cur.execute(sql_command, (result.get('new_ssn'), result.get('ssn')))
                conn.commit()
        return render_template("person_update.html")

    return render_template("person_update.html", personal_list=ssn)

@app.route("/person/add", methods = ['POST', 'GET'])
def person():
    if request.method == 'POST':
        result = request.form
        conn = psycopg2.connect("dbname=guru99 user=okans password=")
        cur = conn.cursor()

        ssn = result.get("ssn")
        personal_name = result.get("personal_name")
        job_title = result.get("job_title")
        email = result.get("email")
        phone_number = result.get("phone_number")

        insert_string = "INSERT INTO personal(ssn, personal_name, job_title, email, phone_number) " \
                        "VALUES(%s, %s, %s, %s, %s);"
        cur.execute(insert_string, (ssn, personal_name, job_title, email, phone_number))
        print("inserted")
        conn.commit()
        return render_template("person.html", result=result,title="Personel Yonetim")

    return render_template("person.html",title="Personel Yonetim")

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
    conn = psycopg2.connect("dbname=guru99 user=okans password=")
    cur = conn.cursor()
    sql_command = "select * from branch"
    cur.execute(sql_command)
    data = cur.fetchall()
    return render_template("depo.html",content=data, title="Depo listesi")

'''
depolarin yonetiminde kullanilacak sayfa
'''
@app.route("/depo/arrange")
def depotArrangnment():
    return render_template("depoArrangment.html",title="Depo listesi")



if __name__=='__main__':
    app.run(debug=True)