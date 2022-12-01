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
def cust_home():
    if 'cust' not in session:
        return redirect('/')
    username = session['cust']
    return render_template('home_cust.html', username=username)

@app.route('/staffHome')
def staff_home():
    if 'staff' not in session:
        return redirect('/')
    username = session['staff']
    return render_template('home_staff.html', username=username)

@app.route('/addAirport')
def add_airport():
    if 'staff' not in session:
        return redirect('/')
    return render_template('add_airport.html')

@app.route('/addAirportPost', methods=['GET', 'POST'])
def add_airportPost():
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
def add_airplane():
    if 'staff' not in session:
        return redirect('/')
    return render_template('add_airplane.html')

@app.route('/addAirplanePost', methods=['GET', 'POST'])
def add_airplanePost():
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

@app.route('/viewFlights')
def view_flights():
    return render_template('view_flights.html', loggedincust='cust' in session)

@app.route('/viewFlightStatusPost', methods=['GET', 'POST'])
def view_flightStatus():
    #grabs information from the forms
    airline_name = request.form['airline_name']
    num = request.form['num']
    dept_date = request.form['dept_date']
    dept_time = request.form['dept_time']

    # May be empty
    arr_date = request.form['arr_date']
    arr_time = request.form['arr_time']
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT status FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    args = [airline_name, num, dept_date, dept_time]
    if arr_date != '':
        query += ' and flight_arrival_date = %s'
        args.append(arr_date)
    if arr_time != '':
        query += ' and flight_arrival_time = %s'
        args.append(arr_time)
    cursor.execute(query, tuple(args))
    data = cursor.fetchone()
    if data is None:
        return render_template('view_flights.html', loggedincust='cust' in session, status='Status: Flight not found')
    else:
        return render_template('view_flights.html', loggedincust='cust' in session, status='Status: ' + data['status'])

@app.route('/searchFlightPost', methods=['GET', 'POST'])
def search_flights():
    #grabs information from the forms as LIKE comparisons
    src_city = '%' + request.form['src_city'] + '%'
    src_airport = '%' + request.form['src_airport'] + '%'
    dest_city = '%' + request.form['dest_city'] + '%'
    dest_airport = '%' + request.form['dest_airport'] + '%'
    dept_date = '%' + request.form['dept_date'] + '%'
    ret_date = '%' + request.form['ret_date'] + '%'

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'CREATE VIEW IF NOT EXISTS departure as (SELECT airport_name as dept_airport_name, city as dept_city FROM airport)'
    cursor.execute(query)
    query = 'CREATE VIEW IF NOT EXISTS arrival as (SELECT airport_name as arrival_airport_name, city as arri_city FROM airport)'
    cursor.execute(query)
    query = 'CREATE VIEW IF NOT EXISTS flight_with_city as (SELECT * FROM flight natural join departure natural join arrival)'
    cursor.execute(query)
    query = 'SELECT * FROM flight_with_city WHERE flight_dept_date > CURDATE() and dept_city like %s and dept_airport_name like %s and arri_city like %s and arrival_airport_name like %s and flight_dept_date like %s'
    args = [src_city, src_airport, dest_city, dest_airport, dept_date]
    if ret_date != '%%':
        query += ' and return_flight_date like %s'
        args.append(ret_date)
    query += ' ORDER BY flight_dept_date, flight_dept_time'
    cursor.execute(query, tuple(args))
    data = cursor.fetchall()
    if len(data) == 0:
        return render_template('view_flights.html', loggedincust='cust' in session, found='No flights were found!')
    else:
        # Convert into table data
        flight_data = []
        for dictionary in data:
            flight_dict = dict()
            flight_dict['airline_name'] = dictionary['airline_name']
            flight_dict['flight_num'] = dictionary['flight_num']
            flight_dict['dept_date'] = str(dictionary['flight_dept_date']) + ' ' + str(dictionary['flight_dept_time'])
            flight_dict['arr_date'] = str(dictionary['flight_arrival_date']) + ' ' + str(dictionary['flight_arrival_time'])
            flight_dict['base_price'] = dictionary['base_price']
            flight_dict['status'] = dictionary['status']
            flight_dict['dept'] = dictionary['dept_airport_name'] + ', ' + dictionary['dept_city']
            flight_dict['arri'] = dictionary['arrival_airport_name'] + ', ' + dictionary['arri_city']

            if dictionary['return_flight_num'] is None:
                flight_dict['return_number'] = 'N/A'
            else:
                flight_dict['return_number'] = dictionary['return_flight_num']
            if dictionary['return_flight_date'] is None:
                flight_dict['return_date'] = 'N/A'
            else:
                flight_dict['return_date'] = str(dictionary['return_flight_date']) + ' ' + str(dictionary['return_flight_time'])
            flight_data.append(flight_dict)
        return render_template('view_flights.html', loggedincust='cust' in session, found=str(len(data)) + ' flights were found', flightdata=flight_data)

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
