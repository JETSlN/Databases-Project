#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='airline_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for customer_login
@app.route('/customerLogin')
def customer_login():
    return render_template('customer_login.html')

#Authenticates the customer_login
@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def customer_loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

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
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        # TODO: Have to change the redirect below
        return redirect(url_for('hello'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customer_login.html', error=error)

#Define route for staff_login
@app.route('/staffLogin')
def staff_login():
    return render_template('staff_login.html')

#Authenticates the staff_login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staff_loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

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
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        # TODO: Have to change the redirect below
        return redirect(url_for('hello'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('customer_login.html', error=error)


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
    password = request.form['password']
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
        error = "This user already exists"
        return render_template('customer_register.html', error = error)
    else:
        ins = 'INSERT INTO customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, name, password, building_num, street, city, state, phone_num, passport_num, passport_exp, passport_country, dob))
        conn.commit()
        cursor.close()
        return render_template('index.html')


#Define route for staff register
@app.route('/staffRegister')
def staff_register():
    return render_template('staff_register.html')

#Authenticates the staff register
@app.route('/staffRegisterAuth', methods=['GET', 'POST'])
def staff_registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['first name']
    lname = request.form['last name']
    airline_name = request.form['airline name']
    dob = request.form['DOB']

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
        error = "This user already exists"
        return render_template('staff_register.html', error = error)
    else:
        ins = 'INSERT INTO airlinestaff VALUES(%s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, fname, lname, dob, airline_name))
        conn.commit()
        cursor.close()
        return render_template('index.html')


"""
TODO: Figure out what session does 
and redirect login pages to appropriate pages
"""


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
