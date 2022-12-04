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

    print(request.args)

    airline_name = request.args['airline_name']
    flight_num = request.args['flight_num']
    dept_date = request.args['dept_date']
    dept_time = request.args['dept_time']
    base_price = request.args['base_price']
    # check flight existence
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s'
    cursor.execute(query, (airline_name, flight_num, dept_date, dept_time))
    data = cursor.fetchall()
    cursor.close()
    if not data:
        return render_template('purchase_ticket.html', badflight='The flight you selected was not found.')
    #create view to see seats
    cursor = conn.cursor()
    query = 'CREATE VIEW IF NOT EXISTS airplane_space as (SELECT * FROM flight natural join airplane natural join ticket)'
    cursor.execute(query)
    query = 'SELECT airline_name, flight_num, flight_dept_date, flight_dept_time, num_seats, base_price, COUNT(*) FROM airplane_space WHERE airline_name = %s and flight_num = %s and flight_dept_date = %s and flight_dept_time = %s GROUP BY airline_name, flight_num, flight_dept_date, flight_dept_time'
    cursor.execute(query, (airline_name, flight_num, dept_date, dept_time))
    data = cursor.fetchone()
    cursor.close()
    if not data:
        session['cust_ticket'] = {"airline_name": airline_name, "flight_num": flight_num, "dept_date": dept_date,
                                  "dept_time": dept_time, "base_price": data['base_price']}
        return render_template('purchase_ticket.html', badflight=False)
    elif data['COUNT(*)'] == data['num_seats']:
        return render_template('purchase_ticket.html', badflight='The flight you selected is full.')
    elif data['COUNT(*)']/data['num_seats'] >= 0.6:
        session['cust_ticket'] = {"airline_name": airline_name, "flight_num": flight_num, "dept_date":dept_date, "dept_time": dept_time, "base_price":(float(data['base_price']) * 1.25)}
        return render_template('purchase_ticket.html', badflight=False)
    else:
        session['cust_ticket'] = {"airline_name": airline_name, "flight_num": flight_num, "dept_date": dept_date,
                                  "dept_time": dept_time, "base_price": data['base_price']}
        return render_template('purchase_ticket.html', badflight=False)


@app.route('/purchaseTicketPost', methods=["GET", "POST"])
def purchaseTicketFormPost():
    airline_name = session['cust_ticket']["airline_name"]
    flight_num = session['cust_ticket']["flight_num"]
    dept_date = session['cust_ticket']["dept_date"]
    dept_time = session['cust_ticket']["dept_time"]
    base_price = session['cust_ticket']["base_price"]
    card_type = request.form['card_type']
    card_name = request.form['card_name']
    card_number = request.form['card_number']
    card_date = request.form['card_date']
    if not card_number.isdigit():
        return render_template('purchase_ticket.html', badflight="Fix card number")
    card_number = int(card_number)
    cursor = conn.cursor()
    query = 'SELECT MAX(CAST(SUBSTRING(ticket_id,4,LENGTH(ticket_id)-3) AS INT)) as l FROM ticket WHERE flight_num = %s'
    cursor.execute(query, flight_num)
    data = cursor.fetchone()
    cursor.close()
    print(data)
    if data:
        max_num = flight_num+"-"+str(int(data['l']) + 1)
    else:
        max_num = flight_num+"-0"
    cursor = conn.cursor()
    ins = 'INSERT INTO ticket VALUES(%s, %s, %s, %s, %s, %s ,%s, %s, %s, %s, %s, CURRENT_DATE(), CURRENT_TIME())'
    cursor.execute(ins, (max_num, flight_num, dept_date, dept_time, airline_name, session['cust'], base_price, card_type, card_number, card_name, card_date))
    conn.commit()
    cursor.close()
    return render_template('purchase_ticket.html', badflight="SUCCESS")


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
    cursor.execute(query, (airline_name, flight_num, dept_date, dept_time))
    data = cursor.fetchall()
    cursor.close()
    if not data:
        pass # TODO error message
    # TODO print results

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
    query = 'SELECT customer, frequency from customer_frequency where frequency = %s'
    cursor.execute(query, most_freq['max(frequency)'])
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
    query = 'SELECT customer_email from ticket where airline_name = %s'
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

    #get all flights of that customer
    cursor = conn.cursor()
    query = 'SELECT * from flight, ticket where flight.flight_num = ticket.flight_num ' \
            'and customer_email = %s and flight.airline_name = %s and flight.airline_name = ticket.airline_name;'
    cursor.execute(query, (customer, (airline_name['airline_name'])))
    data = cursor.fetchall() # holds the airline name the staff works for
    cursor.close()

    return render_template("view_particular_customer_post.html", customer=customer, data=data)

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
    query = 'SELECT airline_name, count(airline_name) as amount from ticket where ' \
            'purchase_date BETWEEN %s and %s and airline_name=%s and customer_email IS NOT NULL;'
    cursor.execute(query, (start_date, end_date, airline_name['airline_name']))
    data = cursor.fetchone() # holds the total amount of tickets sold by the airline
    cursor.close()

    return render_template("view_earned_reports_posts.html", data=data, start_date=start_date, end_date=end_date)

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

    # get earned revenue for past year
    cursor = conn.cursor()
    query = 'select sum(sold_price) as total from ticket ' \
            'where airline_name = %s and purchase_date BETWEEN (CURDATE() - INTERVAL 12 month) and (CURDATE())'
    cursor.execute(query, (airline_name['airline_name']))
    past_yearRev = cursor.fetchone() # holds the revenue for past year
    cursor.close()

    return render_template("view_earned_revenue.html", past_monthRev=past_monthRev, past_yearRev=past_yearRev)

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
