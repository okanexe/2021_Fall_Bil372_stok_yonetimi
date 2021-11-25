from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# db yaratmak için
# createdb -h localhost -p 5432 -U <username> <dbname>
# postgresql bağlanmak için
# psql -h localhost -p 5432 -d postgres

@app.route("/")
def index():
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
        return render_template("person.html", result=result)

    return render_template("person.html")

'''
buradaki dashboad methodu personel ekleme ve personel yonetiminde kullanilacaktir 
'''
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

if __name__=='__main__':
    app.run(debug=True)