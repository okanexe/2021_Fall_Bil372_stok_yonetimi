from flask import Flask, render_template, request, session, redirect, g, url_for
import os
import psycopg2

app = Flask(__name__)
app.secret_key = os.urandom(24)

# db yaratmak için
# createdb -h localhost -p 5432 -U <username> <dbname>
# postgresql bağlanmak için
# psql -h localhost -p 5432 -d postgres

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		session.pop('user', None)
		
		if request.form['password'] == 'password':
			session['user'] = request.form['username']
			return redirect(url_for('protected'))
		
	return render_template('index.html')	
	
@app.route('/protected')
def protected():
 	if g.user:
 		return render_template	('protected.html',user=session['user'])
 	return redirect(url_for('index'))	

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
    
@app.before_request
def before_request():
 	g.user = None
 	
 	if 'user' in session:
 		g.user = session['user']
 		
 		
@app.route('/dropsession')
def dropsession():
	session.pop('user', None)
	return render_template('index.html') 	 		    


'''
    burasi person listelenmesi için kullanilacak
    content array olacak buna gore frontend de basilacak
'''
@app.route("/person/list", methods = ['POST', 'GET'])
def personList():
    return render_template("personList.html")

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


'''
depolarin listelenmesinde kullanilacak olan method
'''
@app.route("/depo/list")
def depotList():
    return render_template("depo.html",title="Depo listesi")

'''
depolarin yonetiminde kullanilacak sayfa
'''
@app.route("/depo/arrange")
def depotArrangnment():
    return render_template("depoArrangment.html",title="Depo listesi")



if __name__=='__main__':
    app.run(debug=True)