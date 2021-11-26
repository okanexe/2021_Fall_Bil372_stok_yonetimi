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
    return render_template("personList.html", content=data,title="Anasayfa")

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
@app.route("/dashboard", methods = ['POST', 'GET'])
def dashboard():
    return render_template("dashboard.html",title="dashboard")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    return render_template("login.html",title="Login")

@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    return render_template("signup.html",title="Sign up")

'''
depolarin listelenmesinde ullanilacak olan method
'''
@app.route("/depo/list", methods = ['POST', 'GET'])
def depot_list():
    content = ["Ford", "Volvo", "BMW"]
    return render_template("depo.html",title="Depo listesi",content=content)

'''
depolarin yonetiminde kullanilacak sayfa
'''
@app.route("/depo/arrange", methods = ['POST', 'GET'])
def depot_arrangnment():
    return render_template("depoArrangment.html",title="Depo listesi")



if __name__=='__main__':
    app.run(debug=True)