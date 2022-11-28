#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib

#Initialize the app from Flask
app = Flask(__name__)
app.debug = True
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airline',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for customer_login
@app.route('/customerLogin')
def customer_login():
    if 'cust' in session:
        return redirect('/custHome')
    return render_template('customer_login.html')

#Authenticates the customer_login
@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def customer_loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE customer_email = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a user session
        session.pop('staff', None)
        session['cust'] = username
        return redirect('/custHome')
    else:
        #returns an error message to the html page
        error = 'Invalid username or password.'
        return render_template('customer_login.html', error=error)

#Define route for staff_login
@app.route('/staffLogin')
def staff_login():
    if 'staff' in session:
        return redirect('/staffHome')
    return render_template('staff_login.html')

#Authenticates the staff_login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staff_loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airlinestaff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a staff session
        session.pop('cust', None)
        session['staff'] = username
        return redirect('/staffHome')
    else:
        #returns an error message to the html page
        error = 'Invalid username or password.'
        return render_template('staff_login.html', error=error)


#Define route for customer register
@app.route('/customerRegister')
def customer_register():
    return render_template('customer_register.html')

#Authenticates the customer register
@app.route('/customerRegisterAuth', methods=['GET', 'POST'])
def customer_registerAuth():
    #grabs information from the forms
    username = request.form['username']
    name = request.form['name']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    street = request.form['street']
    building_num = request.form['Building num']
    city = request.form['City']
    state = request.form['State']
    phone_num = request.form['Phone num']
    passport_exp = request.form['Passport Expiration']
    passport_num = request.form['Passport num']
    passport_country = request.form['Passport Country']
    dob = request.form['DOB']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM customer WHERE customer_email = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists."
        cursor.close()
        return render_template('customer_register.html', error=error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, name, password, building_num, street, city, state, phone_num, passport_num, passport_exp, passport_country, dob))
        conn.commit()
        cursor.close()
        return redirect('/')


#Define route for staff register
@app.route('/staffRegister')
def staff_register():
    return render_template('staff_register.html')

#Authenticates the staff register
@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staff_registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = hashlib.md5(request.form['password'].encode()).hexdigest()
    fname = request.form['first name']
    lname = request.form['last name']
    airline_name = request.form['airline name']
    dob = request.form['DOB']

    #check airline name
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airline WHERE airline_name = %s'
    cursor.execute(query, (airline_name))
    data = cursor.fetchone()
    if not data:
        return render_template('staff_register.html', error="Invalid airline name specified.")

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airlinestaff WHERE username = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This staff already exists."
        cursor.close()
        return render_template('staff_register.html', error=error)
    else:
        ins = 'INSERT INTO airlinestaff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, fname, lname, dob, airline_name))
        conn.commit()
        cursor.close()
        return redirect('/')


@app.route('/custHome')
def custHome():
    if 'cust' not in session:
        return redirect('/')
    username = session['cust']
    return render_template('home_cust.html', username=username)

@app.route('/staffHome')
def staffHome():
    if 'staff' not in session:
        return redirect('/')
    username = session['staff']
    return render_template('home_staff.html', username=username)

@app.route('/addAirport')
def addAirport():
    if 'staff' not in session:
        return redirect('/')
    return render_template('add_airport.html')

@app.route('/addAirportPost', methods=['GET', 'POST'])
def addAirportPost():
    if 'staff' not in session:
        return redirect('/')
    #grabs information from the forms
    name = request.form['name']
    city = request.form['city']
    country = request.form['country']
    type = request.form['type']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airport WHERE airport_name = %s'
    cursor.execute(query, (name))
    data = cursor.fetchone()
    error = None
    if(data):
        error = 'Airport name already exists.'
        cursor.close()
        return render_template('add_airport.html', error=error)
    else:
        ins = 'INSERT INTO airport VALUES(%s, %s, %s, %s)'
        cursor.execute(ins, (name, city, country, type))
        conn.commit()
        cursor.close()
        return redirect('/staffHome')

@app.route('/addAirplane')
def addAirplane():
    if 'staff' not in session:
        return redirect('/')
    return render_template('add_airplane.html')

@app.route('/addAirplanePost', methods=['GET', 'POST'])
def addAirplanePost():
    if 'staff' not in session:
        return redirect('/')
    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    staff_data = cursor.fetchone()
    cursor.close()

    #grabs information from the forms
    id = request.form['id']
    num_seats = request.form['num_seats']
    manu_comp = request.form['manu_comp']
    age = request.form['age']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM airplane WHERE airline_name = %s and airplane_id = %s'
    cursor.execute(query, (staff_data['airline_name'], id))
    data = cursor.fetchone()
    error = None
    if(data):
        error = 'Airplane ID already exists.'
        cursor.close()
        return render_template('add_airplane.html', error=error)
    else:
        ins = 'INSERT INTO airplane VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (staff_data['airline_name'], id, num_seats, manu_comp, age))
        conn.commit()
        cursor.close()
        return redirect('/staffHome')

@app.route('/logout')
def logout():
    session.pop('staff', None)
    session.pop('cust', None)
    return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
