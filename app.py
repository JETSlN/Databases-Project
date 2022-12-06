#Import Flask Library
from flask import Flask, render_template, request, session, redirect
from datetime import date, timedelta, datetime
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
        session.pop('cust_ticket', None)
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
    phone = request.form['phonenum']
    email = request.form['email']
    phone = phone.split(",")
    email = email.split(",")

    for x in phone:
        try:
            int(x)
        except:
            return render_template('staff_register.html', error="Invalid number use number format")



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
        for x in phone:
            cursor = conn.cursor()
            ins = 'INSERT INTO staffphone VALUES(%s, %s)'
            cursor.execute(ins, (username, x.strip()))
            conn.commit()
            cursor.close()
        for x in email:
            cursor = conn.cursor()
            ins = 'INSERT INTO staffemail VALUES(%s, %s)'
            cursor.execute(ins, (username, x.strip()))
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

@app.route('/addFlight')
def add_flight():
    if 'staff' not in session:
        return redirect('/')
    return render_template('add_flight.html')

@app.route('/addFlightPost', methods=['GET', 'POST'])
def add_flightPost():
    if 'staff' not in session:
        return redirect('/')
    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    staff_data = cursor.fetchone()
    cursor.close()

    #grabs information from the forms
    flight_num = request.form['flight_num']
    flight_dept_date = request.form['flight_dept_date']
    flight_dept_time = request.form['flight_dept_time']
    flight_arrival_date = request.form['flight_arrival_date']
    flight_arrival_time = request.form['flight_arrival_time']
    base_price = request.form['base_price']
    dept_airport_name = request.form['dept_airport_name']
    arrival_airport_name = request.form['arrival_airport_name']
    airplane_id = request.form['airplane_id']
    status = request.form['status']

    try:
        float(base_price)
    except:
        error = 'Price not a float num'
        return render_template('add_flight.html', error=error)
    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT (CURRENT_DATE() + INTERVAL 1 DAY) as days'
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()
    if str(data["days"]) > str(flight_dept_date):
        error = 'Airplane date past already'
        return render_template('add_flight.html', error=error)

    if flight_dept_date > flight_arrival_date or (flight_dept_date >= flight_arrival_date and flight_dept_time > flight_arrival_date):
        error = 'Airplane can not arrive before departure'
        return render_template('add_flight.html', error=error)

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'Select * FROM airport WHERE airport_name = %s'
    cursor.execute(query, dept_airport_name)
    data = cursor.fetchone()
    cursor.close()

    if not data:
        error = 'Departure airport does not exist'
        return render_template('add_flight.html', error=error)

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'Select * FROM airport WHERE airport_name = %s'
    cursor.execute(query, arrival_airport_name)
    data = cursor.fetchone()
    cursor.close()

    if not data:
        error = 'Arrival airport does not exist'
        return render_template('add_flight.html', error=error)

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'Select * FROM airplane WHERE airplane_id = %s and airline_name = %s'
    cursor.execute(query, (airplane_id, staff_data['airline_name']))
    data = cursor.fetchone()
    cursor.close()

    if not data:
        error = 'Airplane does not exist'
        return render_template('add_flight.html', error=error)

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (staff_data['airline_name'], flight_num, flight_dept_date, flight_dept_time))
    data = cursor.fetchone()
    cursor.close()
    error = None
    if(data):
        error = 'Airplane ID already exists.'
        return render_template('add_flight.html', error=error)
    else:
        # Check if departure flight is valid (link this flight as a return flight)
        link_flight = False
        if request.form['dept_flight_num'] and request.form['dept_flight_date'] and request.form['dept_flight_time']:
            cursor = conn.cursor()
            query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
            cursor.execute(query, (staff_data['airline_name'], request.form['dept_flight_num'], request.form['dept_flight_date'], request.form['dept_flight_time']))
            cursor.close()
            data = cursor.fetchone()
            if data is None:
                return render_template('add_flight.html', error="Departure flight linked is invalid.")
            if data['return_flight_num']:
                return render_template('add_flight.html', error="Departure flight is already linked to a return flight.")
            link_flight = True

        cursor = conn.cursor()
        ins = 'INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL, NULL, NULL)'
        cursor.execute(ins, (staff_data['airline_name'], flight_num, flight_dept_date, flight_dept_time, flight_arrival_date, flight_arrival_time, base_price, status, dept_airport_name, arrival_airport_name, airplane_id))
        conn.commit()
        cursor.close()

        if link_flight:
            cursor = conn.cursor()
            ins = 'UPDATE flight SET return_flight_num = %s, return_flight_date = %s, return_flight_time = %s WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
            cursor.execute(ins, (flight_num, flight_dept_date, flight_dept_time, staff_data['airline_name'], request.form['dept_flight_num'], request.form['dept_flight_date'], request.form['dept_flight_time']))
            conn.commit()
            cursor.close()

        return redirect('/staffHome')

@app.route('/addRating')
def add_rating():
    if 'cust' not in session:
        return redirect('/')

    airline_name = request.args['airline_name']
    flight_num = request.args['flight_num']
    flight_dept_date = request.args['dept_date']
    flight_dept_time = request.args['dept_time']
    info = {'name': airline_name, 'num': flight_num, 'date': flight_dept_date, 'time': flight_dept_time}

    flight_arr_date = request.args['arr_date'].split()[0]
    flight_arr_time = request.args['arr_date'].split()[1]

    session['custRating'] = {'name': airline_name, 'num': flight_num, 'date': flight_dept_date,
                             'time': flight_dept_time, "date2": flight_arr_date, "time2":flight_arr_time}
    return render_template('add_rating.html', error = False, info = info)

@app.route('/addRatingPost', methods=['GET', 'POST'])
def add_ratingPost():
    if 'cust' not in session:
        return redirect('/')
    #grabs information from the forms

    rate = request.form['rate']
    comment = request.form['comment']
    airline_name = session['custRating']['name']
    flight_num = session['custRating']['num']
    flight_dept_date = session['custRating']['date']
    flight_dept_time = session['custRating']['time']
    flight_arr_date = session['custRating']['date2']
    flight_arr_time = session['custRating']['time2']
    cust = session['cust']
    info = {'name': airline_name, 'num': flight_num, 'date': flight_dept_date, 'time': flight_dept_time}
    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM review WHERE customer_email = %s AND airline_name = %s AND flight_num = %s AND flight_dept_date = %s AND flight_dept_time = %s'

    cursor.execute(query, (cust, airline_name, flight_num, flight_dept_date, flight_dept_time))
    data = cursor.fetchone()
    error = None
    cursor.close()
    if (data):
        error = 'Rating already exists.'
        cursor.close()
        return render_template('add_rating.html', badrating="Rating already exists",error=False, info=info)

    cursor = conn.cursor()
    query = 'SELECT CURRENT_DATE() as days, CURRENT_TIME() as times'
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    if (str(data["days"]) < str(flight_arr_date)) or (
            str(data["days"]) == str(flight_arr_date) and str(data["times"]) < str(flight_arr_time)):
        error = 'Your flight is not completed yet'
        return render_template('add_rating.html', badrating='Your flight is not completed yet', error=error, info=info)



    try:
        float(rate)
    except:
        error = 'Invalid rating please rate from 0-5 stars'
        return render_template('add_rating.html', error=error, info=info, badrating=False)

    if float(rate) < 0 or float(rate) > 5:
        error = 'Invalid rating please rate from 0-5 stars'
        return render_template('add_rating.html', error=error, info=info,  badrating=False)

    cursor = conn.cursor()
    ins = 'INSERT INTO review VALUES(%s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (cust, airline_name, flight_num, flight_dept_date, flight_dept_time, rate, comment))
    conn.commit()
    cursor.close()
    session.pop('custRating', None)
    return render_template('add_rating.html', badrating="Ticket successfully purchased!", error=False)

@app.route('/viewFutureFlights')
def view_future_flights():
    return render_template('view_future_flights.html', loggedincust='cust' in session)

@app.route('/viewFlightStatusPost', methods=['GET', 'POST'])
def view_flight_status():
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
    cursor.close()
    if data is None:
        return render_template('view_future_flights.html', loggedincust='cust' in session, status='Status: Flight not found')
    else:
        return render_template('view_future_flights.html', loggedincust='cust' in session, status='Status: ' + data['status'])

@app.route('/searchFutureFlightsPost', methods=['GET', 'POST'])
def search_future_flights():
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
    cursor.close()
    if len(data) == 0:
        return render_template('view_future_flights.html', loggedincust='cust' in session, found='No flights were found!')
    else:
        # Convert into table data
        flight_data = []
        for dictionary in data:
            flight_dict = dict()
            flight_dict['airline_name'] = dictionary['airline_name']
            flight_dict['flight_num'] = dictionary['flight_num']
            flight_dict['dept_date'] = str(dictionary['flight_dept_date'])
            flight_dict['dept_time'] = str(dictionary['flight_dept_time'])
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
        return render_template('view_future_flights.html', loggedincust='cust' in session, found=str(len(data)) + ' flights were found', flightdata=flight_data)

@app.route('/viewAirlineFlights')
def view_airline_flights():
    if 'staff' not in session:
        return redirect('/')
    message = "Search for your airline's flights below:"
    start_date = date.today()
    end_date = date.today() + timedelta(days=30)
    return render_template('view_all_flights.html', staff=True, message=message, startdate=start_date, enddate=end_date)

@app.route('/viewMyFlights')
def view_cust_flights():
    if 'cust' not in session:
        return redirect('/')
    message = "Search for your purchased tickets below:"
    start_date = date.today()
    end_date = ''
    return render_template('view_all_flights.html', staff=False, message=message, startdate=start_date, enddate=end_date)

@app.route('/searchFlightsPost', methods=['GET', 'POST'])
def search_flights():
    is_staff = 'staff' in session
    if not is_staff and 'cust' not in session:
        return redirect('/')

    if is_staff:
        message = "Search for your airline's flights below:"
    else:
        message = "Search for your purchased tickets below:"

    #grabs information from the forms as LIKE comparisons (except for the date range)
    src_city = '%' + request.form['src_city'] + '%'
    src_airport = '%' + request.form['src_airport'] + '%'
    dest_city = '%' + request.form['dest_city'] + '%'
    dest_airport = '%' + request.form['dest_airport'] + '%'
    dept_date_start = request.form['dept_date_start']
    dept_date_end = request.form['dept_date_end']

    #cursor used to send queries
    cursor = conn.cursor()

    staff_data = None
    if is_staff:
        query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
        cursor.execute(query, (session['staff']))
        staff_data = cursor.fetchone()

    #executes query
    query = 'CREATE VIEW IF NOT EXISTS departure as (SELECT airport_name as dept_airport_name, city as dept_city FROM airport)'
    cursor.execute(query)
    query = 'CREATE VIEW IF NOT EXISTS arrival as (SELECT airport_name as arrival_airport_name, city as arri_city FROM airport)'
    cursor.execute(query)
    query = 'CREATE VIEW IF NOT EXISTS flight_with_city as (SELECT * FROM flight natural join departure natural join arrival)'
    cursor.execute(query)

    if is_staff:
        # Must only select from staff's airline
        query = 'SELECT * FROM flight_with_city WHERE airline_name = %s and dept_city like %s and dept_airport_name like %s and arri_city like %s and arrival_airport_name like %s'
        args = [staff_data['airline_name'], src_city, src_airport, dest_city, dest_airport]
    else:
        # Select flights that the user purchased
        query = 'SELECT * FROM flight_with_city natural join ticket WHERE customer_email = %s and dept_city like %s and dept_airport_name like %s and arri_city like %s and arrival_airport_name like %s'
        args = [session['cust'], src_city, src_airport, dest_city, dest_airport]
    if dept_date_start:
        query += ' and flight_dept_date >= %s'
        args.append(dept_date_start)
    if dept_date_end:
        query += ' and flight_dept_date <= %s'
        args.append(dept_date_end)

    query += ' ORDER BY flight_dept_date, flight_dept_time'
    cursor.execute(query, tuple(args))
    data = cursor.fetchall()
    if len(data) == 0:
        return render_template('view_all_flights.html', staff=is_staff, found='No flights were found!', message=message)
    else:
        # Convert into table data
        flight_data = []
        for dictionary in data:
            flight_dict = dict()
            flight_dict['airline_name'] = dictionary['airline_name']
            flight_dict['flight_num'] = dictionary['flight_num']
            flight_dict['dept_date'] = str(dictionary['flight_dept_date'])
            flight_dict['dept_time'] = str(dictionary['flight_dept_time'])
            flight_dict['arr_date'] = str(dictionary['flight_arrival_date']) + ' ' + str(dictionary['flight_arrival_time'])
            flight_dict['base_price'] = dictionary['base_price']
            flight_dict['status'] = dictionary['status']
            flight_dict['dept'] = dictionary['dept_airport_name'] + ', ' + dictionary['dept_city']
            flight_dict['arri'] = dictionary['arrival_airport_name'] + ', ' + dictionary['arri_city']

            if not is_staff:
                flight_dict['ticket_id'] = dictionary['ticket_id']
                flight_dict['paid_price'] = dictionary['sold_price']
                flight_dict['purchase_date'] = str(dictionary['purchase_date']) + ' ' + str(dictionary['purchase_time'])

            if dictionary['return_flight_num'] is None:
                flight_dict['return_number'] = 'N/A'
            else:
                flight_dict['return_number'] = dictionary['return_flight_num']
            if dictionary['return_flight_date'] is None:
                flight_dict['return_date'] = 'N/A'
            else:
                flight_dict['return_date'] = str(dictionary['return_flight_date']) + ' ' + str(dictionary['return_flight_time'])
            flight_data.append(flight_dict)
        if is_staff:
            found = str(len(data)) + ' flights were found'
        else:
            found = str(len(data)) + ' tickets were found'
        return render_template('view_all_flights.html', staff=is_staff, found=found, flightdata=flight_data, message=message)

@app.route('/purchaseTicket')
def purchaseTicketForm():
    if 'cust' not in session:
        return redirect('/')

    airline_name = request.args['airline_name']
    flight_num = request.args['flight_num']
    dept_date = request.args['dept_date']
    dept_time = request.args['dept_time']
    # check flight existence
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (airline_name, flight_num, dept_date, dept_time))
    data = cursor.fetchone()
    cursor.close()
    if not data:
        return render_template('purchase_ticket.html', badflight='The flight you selected was not found.')
    base_price = data['base_price']
    #create view to see seats
    cursor = conn.cursor()
    query = 'CREATE VIEW IF NOT EXISTS airplane_space as (SELECT * FROM flight natural join airplane natural join ticket)'
    cursor.execute(query)
    query = 'SELECT airline_name, flight_num, flight_dept_date, flight_dept_time, num_seats, base_price, COUNT(*) FROM airplane_space WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s GROUP BY airline_name, flight_num, flight_dept_date, flight_dept_time'
    cursor.execute(query, (airline_name, flight_num, dept_date, dept_time))
    data = cursor.fetchone()
    cursor.close()

    # Note: Data is empty if flight seats are empty
    info = {'name': airline_name, 'num': flight_num, 'date': dept_date, 'time': dept_time}
    if data and data['COUNT(*)'] >= data['num_seats']:
        return render_template('purchase_ticket.html', badflight='The flight you selected is full.')
    elif data and data['COUNT(*)']/data['num_seats'] >= 0.6:
        actual_cost = float(base_price) * 1.25
        info['cost'] = actual_cost
        info['extra'] = True
        session['cust_ticket'] = {"airline_name": airline_name, "flight_num": flight_num, "dept_date":dept_date, "dept_time": dept_time, "price": actual_cost}
        return render_template('purchase_ticket.html', badflight=False, info=info)
    else:
        info['cost'] = base_price
        session['cust_ticket'] = {"airline_name": airline_name, "flight_num": flight_num, "dept_date": dept_date,
                                  "dept_time": dept_time, "price": base_price}
        return render_template('purchase_ticket.html', badflight=False, info=info)


@app.route('/purchaseTicketPost', methods=["GET", "POST"])
def purchaseTicketFormPost():
    if 'cust' not in session or 'cust_ticket' not in session:
        return redirect('/')
    airline_name = session['cust_ticket']["airline_name"]
    flight_num = session['cust_ticket']["flight_num"]
    dept_date = session['cust_ticket']["dept_date"]
    dept_time = session['cust_ticket']["dept_time"]
    base_price = session['cust_ticket']["price"]
    card_type = request.form['card_type']
    card_name = request.form['card_name']
    card_number = request.form['card_number']
    card_date = request.form['card_date']

    if not card_number.isdigit():
        return render_template('purchase_ticket.html', badflight="Purchase failed (bad card number).")
    card_number = int(card_number)

    cursor = conn.cursor()

    # select next ID
    query = 'SELECT CURRENT_DATE() as dates'
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    if str(data['dates']) >= str(card_date):
        return render_template('purchase_ticket.html', badflight="Your card expired")

    cursor = conn.cursor()

    # select next ID
    query = 'SELECT MAX(CAST(SUBSTRING(ticket_id,%s,LENGTH(ticket_id)) AS INT)) as l FROM ticket WHERE flight_num = %s and airline_name = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (len(flight_num) + 2, flight_num, airline_name, dept_date, dept_time))
    data = cursor.fetchone()
    cursor.close()

    if data and data['l'] is not None:
        max_num = flight_num+"-"+str(int(data['l']) + 1)
    else:
        max_num = flight_num+"-0"
    cursor = conn.cursor()
    ins = 'INSERT INTO ticket VALUES(%s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s, CURRENT_DATE(), CURRENT_TIME())'
    cursor.execute(ins, (max_num, flight_num, dept_date, dept_time, airline_name, session['cust'], base_price, card_type, card_number, card_name, card_date))
    conn.commit()
    cursor.close()
    session.pop('cust_ticket', None)
    return render_template('purchase_ticket.html', badflight="Ticket successfully purchased!")


@app.route('/cancelTrip')
def cancel_trip():
    if 'cust' not in session:
        return redirect('/')
    ticket_id = request.args['ticket_id']

    # check ticket existance
    cursor = conn.cursor()
    query = 'SELECT * FROM ticket WHERE ticket_id = %s and customer_email = %s'
    cursor.execute(query, (ticket_id, session['cust']))
    data = cursor.fetchone()
    cursor.close()
    if not data:
        return render_template('cancel_trip.html', error="Error: The ticket you selected was not found.")

    # check if flight is at lesat 24 hours from today
    flight_time = datetime.combine(data['flight_dept_date'], datetime.min.time()) + data['flight_dept_time']
    time_diff = flight_time - datetime.now()
    if time_diff < timedelta(hours=24):
        return render_template('cancel_trip.html', error="Error: The flight you selected is not at least 24 hours from today.")

    # cancel trip
    cursor = conn.cursor()
    query = 'DELETE FROM ticket WHERE ticket_id = %s and customer_email = %s'
    cursor.execute(query, (ticket_id, session['cust']))
    cursor.close()

    success = 'Successfully cancelled ticket {} from flight {} with departure time {} {}.'.format(ticket_id, data['flight_num'], data['flight_dept_date'], data['flight_dept_time'])
    return render_template('cancel_trip.html', success=success)

@app.route('/viewCustomers')
def view_customers():
    if 'staff' not in session:
        return redirect('/')
    flight_num = request.args['flight_num']
    dept_date = request.args['dept_date']
    dept_time = request.args['dept_time']

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    # check flight existance
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (airline_name['airline_name'], flight_num, dept_date, dept_time))
    data = cursor.fetchall()
    cursor.close()
    if not data:
        return render_template("view_flights_customers.html", message="The flight you selected does not exist")
    message = None
    cursor = conn.cursor()
    query = 'SELECT customer_email as customer from ticket where airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (airline_name['airline_name'], flight_num, dept_date, dept_time))
    data1 = cursor.fetchall() # all the customer emails selected by the above query
    cursor.close()

    if not data1:
        message = "There are no customers for the flight you selected"
        return render_template("view_flights_customers.html", message=message)


    return render_template("view_flights_customers.html", data1=data1)

@app.route('/viewRatings')
def view_ratings():
    if 'staff' not in session:
        return redirect('/')
    flight_num = request.args['flight_num']
    dept_date = request.args['dept_date']
    dept_time = request.args['dept_time']

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    # check flight existance
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (airline_name['airline_name'], flight_num, dept_date, dept_time))
    data = cursor.fetchall()
    cursor.close()
    if not data:
        return render_template("view_flights_rating.html", message="The flight you selected does not exist")

    # Get average ratings of the flight selected
    cursor = conn.cursor()
    query = 'SELECT AVG(rating) as average_rating from review where airline_name = %s and flight_dept_date = %s and flight_dept_time = %s and flight_num = %s'
    cursor.execute(query, (airline_name['airline_name'], dept_date, dept_time, flight_num))
    average_rating = cursor.fetchone() # Holds the average rating of the flight selected
    cursor.close()

    # Get the ratings and comments of each customer for the fligt selected
    cursor = conn.cursor()
    query = 'SELECT customer_email as customer, rating, comments from review where airline_name = %s and flight_dept_date = %s and flight_dept_time = %s and flight_num = %s'
    cursor.execute(query, (airline_name['airline_name'], dept_date, dept_time, flight_num))
    data = cursor.fetchall() # Holds all the customer's ratings for the flight
    cursor.close()

    if not data:
        return render_template("view_flights_rating.html", message="There are no ratings or comments for the flight selected")

    return render_template("view_flights_rating.html", average_rating=average_rating, data=data, message=None)


@app.route('/viewmostfreqcust')
def view_most_freq_customer():
    if 'staff' not in session:
        return redirect('/')

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #create or replace a view
    cursor = conn.cursor()
    query = 'CREATE OR REPLACE VIEW customer_frequency AS ' \
            'SELECT customer_email as customer, count(customer_email) as frequency, airline_name ' \
            'from ticket ' \
            'where purchase_date BETWEEN (CURDATE() - INTERVAL 12 month) and (CURDATE())' \
            'group by customer_email, airline_name;'
    cursor.execute(query)
    cursor.close()

    #get frequency of most frequent customer for that airline
    cursor = conn.cursor()
    query = 'SELECT max(frequency) from customer_frequency WHERE airline_name = %s'
    cursor.execute(query, (airline_name['airline_name']))
    most_freq = cursor.fetchone() # holds most frequent customer
    cursor.close()

    #get a list of the most frequent customers
    cursor = conn.cursor()
    query = 'SELECT customer, frequency from customer_frequency where frequency = %s and airline_name = %s'
    cursor.execute(query, (most_freq['max(frequency)'], airline_name['airline_name']))
    data = cursor.fetchall() # holds the [most frequent customer, frequency]
    cursor.close()

    return render_template('view_most_frequent_customer.html', data=data, airline_name=airline_name)

@app.route('/view_part_customer')
def view_particular_customer():
    if 'staff' not in session:
        return redirect('/')

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #get list of customer for that airline
    cursor = conn.cursor()
    query = 'SELECT DISTINCT customer_email from ticket where airline_name = %s'
    cursor.execute(query, airline_name['airline_name'])
    data = cursor.fetchall() # holds a list of customers for that airline
    cursor.close()


    return render_template('view_particular_customer.html', data=data)

@app.route('/view_particular_customer_post', methods = ['GET', 'POST'])
def view_particular_customer_post():
    if 'staff' not in session:
        return redirect('/')
    customer = request.form['customer']

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #Check if customer exists
    cursor = conn.cursor()
    query = 'SELECT * from ticket where airline_name = %s and customer_email = %s'
    cursor.execute(query, (airline_name['airline_name'], customer))
    data = cursor.fetchone() # holds a list of customers for that airline
    cursor.close()

    if not data:
        return render_template("view_particular_customer_post.html", error="This customer doesn't exist, please provide a correct customer email")

    #get all flights of that customer
    cursor = conn.cursor()
    query = 'SELECT * from flight, ticket where flight.flight_num = ticket.flight_num ' \
            'and customer_email = %s and flight.airline_name = %s and flight.airline_name = ticket.airline_name and flight.flight_dept_date = ticket.flight_dept_date and flight.flight_dept_time = ticket.flight_dept_time;'
    cursor.execute(query, (customer, (airline_name['airline_name'])))
    data = cursor.fetchall() # holds the airline name the staff works for
    cursor.close()

    return render_template("view_particular_customer_post.html", customer=customer, data=data, error=None)

@app.route('/view_earned_reports')
def view_earned_reports():
    if 'staff' not in session:
        return redirect('/')
    return render_template("view_earned_reports.html")

@app.route('/view_earned_reportsPost', methods = ['GET', 'POST'])
def view_earned_reports_post():
    if 'staff' not in session:
        return redirect('/')
    start_date = request.form['Start Date']
    end_date = request.form['End Date']

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #get total amount of tickets sold by that airline
    cursor = conn.cursor()
    query = 'SELECT airline_name, count(ticket_id) as amount from ticket where ' \
            'purchase_date BETWEEN %s and %s and airline_name=%s and customer_email IS NOT NULL;'
    cursor.execute(query, (start_date, end_date, airline_name['airline_name']))
    data = cursor.fetchone() # holds the total amount of tickets sold by the airline
    cursor.close()

    # get the tickets sold month-wise
    cursor = conn.cursor()
    query = 'SELECT Month(purchase_date), count(ticket_id) from ticket where purchase_date BETWEEN %s and %s and airline_name = %s and customer_email is not NULL group by Month(purchase_date)'
    cursor.execute(query, (start_date, end_date, airline_name['airline_name']))
    data1 = cursor.fetchall()
    cursor.close()


    month = {'01':'Janauary','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}

    if data1:
        for line in data1:
            line['Month(purchase_date)'] = month[str(line['Month(purchase_date)'])]
    else:
        data1 = None

    return render_template("view_earned_reports_posts.html", data=data, start_date=start_date, end_date=end_date, data1=data1)

@app.route('/view_earned_revenue')
def view_earned_revenue():
    if 'staff' not in session:
        return redirect('/')

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #get Earned revenue in last month
    cursor = conn.cursor()
    query = 'select sum(sold_price) as total from ticket ' \
            'where airline_name = %s and purchase_date BETWEEN (CURDATE() - INTERVAL 1 month) and (CURDATE())'
    cursor.execute(query, (airline_name['airline_name']))
    past_monthRev = cursor.fetchone() # holds the revenue for past month
    cursor.close()

    if not past_monthRev['total']:
        past_monthRev['total'] = 0

    # get earned revenue for past year
    cursor = conn.cursor()
    query = 'select sum(sold_price) as total from ticket ' \
            'where airline_name = %s and purchase_date BETWEEN (CURDATE() - INTERVAL 12 month) and (CURDATE())'
    cursor.execute(query, (airline_name['airline_name']))
    past_yearRev = cursor.fetchone() # holds the revenue for past year
    cursor.close()

    if not past_yearRev['total']:
        past_yearRev['total'] = 0

    return render_template("view_earned_revenue.html", past_monthRev=past_monthRev, past_yearRev=past_yearRev)

@app.route('/change_flight_status')
def change_flight_status():
    if 'staff' not in session:
        return redirect('/')

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #get all flights operated by the airline
    cursor = conn.cursor()
    query = 'SELECT flight_num, flight_dept_date, flight_dept_time, status ' \
            'from flight ' \
            'where airline_name = %s'
    cursor.execute(query, airline_name['airline_name'])
    data1 = cursor.fetchall() # holds a list of all the flights operated by the airline
    cursor.close()

    return render_template('change_flight_status.html', airline_name=airline_name, data1=data1)

@app.route('/change_flight_status_post', methods=['GET', 'POST'])
def change_flight_status_post():
    if 'staff' not in session:
        return redirect('/')

    #get airline name
    cursor = conn.cursor()
    query = 'SELECT airline_name FROM airlinestaff WHERE username = %s'
    cursor.execute(query, (session['staff']))
    airline_name = cursor.fetchone() # holds the airline name the staff works for
    cursor.close()

    #get all flights operated by the airline
    cursor = conn.cursor()
    query = 'SELECT flight_num, flight_dept_date, flight_dept_time, status ' \
            'from flight ' \
            'where airline_name = %s'
    cursor.execute(query, airline_name['airline_name'])
    data1 = cursor.fetchall() # holds a list of all the flights operated by the airline
    cursor.close()

    flight_num = request.form['flight num']
    flight_dept_date = request.form['flight date']
    flight_dept_time = request.form['flight time']
    status = request.form['status']

    #check if flight exists in the table
    cursor = conn.cursor()
    query = 'SELECT airline_name, flight_num, flight_dept_date, flight_dept_time ' \
            'from flight ' \
            'where airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (airline_name['airline_name'], flight_num, flight_dept_date, flight_dept_time))
    data = cursor.fetchone() # holds the flight specified
    cursor.close()
    error = None

    if not data:
        #If the previous query doesn't return data, then the flight doesn't exist
        error = "This Flight doesn't exist, please make sure to input the correct information for the flight you would like to change the status for"
        return render_template('change_flight_status.html', error=error, airline_name=airline_name, data1=data1)
    else:
        cursor = conn.cursor()
        query = 'UPDATE flight ' \
                'set status = %s ' \
                'where airline_name = %s and flight_num = %s' \
                                               'and flight_dept_date = %s and flight_dept_time = %s'
        cursor.execute(query, (status, airline_name['airline_name'], flight_num, flight_dept_date, flight_dept_time))
        conn.commit()
        cursor.close()
        return redirect('/change_flight_status')

@app.route('/trackSpending')
def track_spending():
    if 'cust' not in session:
        redirect('/')
    start_date = date.today() - timedelta(days=365)
    end_date = date.today()
    return render_template('track_spending.html', startdate=start_date, enddate=end_date)

@app.route('/trackSpendingPost', methods=['GET', 'POST'])
def track_spending_post():
    if 'cust' not in session:
        redirect('/')

    start = request.form['start']
    end = request.form['end']

    # filter by date and split into months
    cursor = conn.cursor()
    query = 'SELECT YEAR(purchase_date) as y, MONTH(purchase_date) as m, sum(sold_price) as s FROM ticket WHERE customer_email = %s and purchase_date >= %s and purchase_date <= %s' \
            ' GROUP BY YEAR(purchase_date), MONTH(purchase_date) ORDER BY purchase_date DESC'
    cursor.execute(query, (session['cust'], start, end))
    data = cursor.fetchall()

    cursor = conn.cursor()
    query = 'SELECT sum(sold_price) as s FROM ticket WHERE customer_email = %s and purchase_date >= %s and purchase_date <= %s'
    cursor.execute(query, (session['cust'], start, end))
    total = cursor.fetchone()

    if not data:
        found = None
    else:
        found = '${} was spent over {} distinct months. View additional information below:'.format(total['s'], len(data))
    return render_template('track_spending.html', data=data, found=found)


@app.route('/logout')
def logout():
    session.pop('staff', None)
    session.pop('cust', None)
    session.pop('cust_ticket', None)
    return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
