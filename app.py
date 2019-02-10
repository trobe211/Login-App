from flask import Flask, request, render_template, redirect
from sqlite3 import *
import jinja2


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/result', methods=['POST','GET'])
# The form in the HTML document sends the user to /result
def result():
    if request.method == 'POST': # Check if they were sent from the form
        conn = connect('mydatabase.db')  # Connect to the database
        db = conn.cursor()
        # Check if username is in database
        db.execute('''SELECT * FROM Users where Username = "{0}"'''.format(request.form['username'].upper()))
        rows = db.fetchall()
        # Check if the result of that query is greater than 0, meaning it returned something
        if len(rows) > 0:
            # Usernames are unique, therefore only check first set of data to see if passwords match
            if rows[0][1] == request.form['password'].upper():
                return '<h1>You have been successfully logged in </h1>'
        return render_template('invalid.html')


@app.route('/register')
# The form in the HTML document sends the user to /result
def register():
    return render_template('register.html')

@app.route('/register-result', methods=['POST','GET'])
# The form in the HTML document sends the user to /result
def registerResult():
    if request.method == 'POST': # Check if they were sent from the form
        conn = connect('mydatabase.db')  # Connect to the database
        db = conn.cursor()
        # Check if username is in database
        db.execute('''SELECT * FROM Users where Username = "{0}"'''.format(request.form['username'].upper()))
        rows = db.fetchall()
        # Check if the result of that query is greater than 0, meaning it returned something
        if len(rows) > 0:
            # Return the template which states that username is taken
            conn.close()
            return render_template('taken.html')
        else:
            db.execute('''INSERT INTO Users VALUES ("{0}" , "{1}");'''.format(request.form['username'].upper(),request.form['password'].upper()))
            conn.commit()
            conn.close()
            return "<h1>You have been successfully registered </h1>"




if __name__ == '__main__':
    app.run(debug=True)