from flask import Flask, render_template, request, redirect, session, url_for
import pymysql
from config import DATABASE_CONFIG

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection
db = pymysql.connect(**DATABASE_CONFIG)
cursor = db.cursor()

# Create users table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

# Create addresses table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    city VARCHAR(255),
    state VARCHAR(255),
    zipcode VARCHAR(10),
    birthday VARCHAR(20),
    email VARCHAR(255),
    phone1 VARCHAR(20),
    phone2 VARCHAR(20),
    comment TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")
db.commit()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect(url_for('menu'))
    else:
        return "Login failed. Please check your username and password."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return redirect(url_for('registration_success'))

    return render_template('registration.html')

@app.route('/registration_success')
def registration_success():
    return render_template('registration_success.html')

@app.route('/menu')
def menu():
    if 'username' in session:
        return render_template('menu.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/entry', methods=['GET', 'POST'])
def data_entry():
    if request.method == 'POST':
        user_id = session['user_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipcode = request.form['zipcode']
        birthday = request.form['birthday']
        email = request.form['email']
        phone1 = request.form['phone1']
        phone2 = request.form['phone2']
        comment = request.form['comment']

        cursor.execute("""
            INSERT INTO addresses (user_id, firstname, lastname, address, city, state, zipcode, birthday, email, phone1, phone2, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, firstname, lastname, address, city, state, zipcode, birthday, email, phone1, phone2, comment))
        db.commit()

        return redirect(url_for('display_records'))

    return render_template('data_entry.html')

@app.route('/display_records', methods=['GET', 'POST'])
def display_records():
    if request.method == 'POST':
        firstname = request.form.get('firstname')
        cursor.execute("SELECT * FROM addresses WHERE firstname LIKE %s AND user_id=%s", ('%' + firstname + '%', session['user_id']))
    else:
        cursor.execute("SELECT * FROM addresses WHERE user_id=%s", (session['user_id'],))

    records = cursor.fetchall()
    return render_template('display_records.html', records=records)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='192.168.12.2', port=5000, debug=True)
