#!/home/al/miniconda3/envs/py/bin/python3
# -*- coding: utf-8 -*-
#
# filename:   /home/al/projects/AddressBook_v2/app.py
#
# v2.3: Adds the route for viewing full contact details.

from flask import Flask, render_template, request, redirect, session, url_for, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import sys
sys.path.append('/home/al/py')
from MySql import MySQL
import config
import OV_addressbook

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
db = MySQL(**config.mysql_config)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("You must be logged in to view this page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# --- User Routes (Unchanged) ---
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = db.get_data("SELECT id, username, password_hash FROM users WHERE username = %s", (username,))
        if user_data and check_password_hash(user_data[0]['password_hash'], password):
            session['user_id'] = user_data[0]['id']
            session['username'] = user_data[0]['username']
            flash(f"Welcome back, {session['username']}!", "success")
            return redirect(url_for('list_contacts_route'))
        else:
            flash("Login failed.", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        comment = request.form.get('comment')
        if db.get_data("SELECT id FROM users WHERE username = %s", (username,)):
            flash("That username is already taken.", "error")
            return render_template('register.html')
        password_hash = generate_password_hash(password)
        query = """
            INSERT INTO users (username, password_hash, firstname, lastname, address, city, state,
                               zipcode, birthday, email, phone1, phone2, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (username, password_hash, firstname, lastname, address, city, state,
                  zipcode, birthday, email, phone1, phone2, comment)
        db.put_data(query, params)
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# --- Application Routes ---
@app.route('/contacts')
@login_required
def list_contacts_route():
    return OV_addressbook.list_contacts()

# --- NEW ROUTE ---
@app.route('/contacts/view/<int:contact_id>')
@login_required
def view_contact_route(contact_id):
    return OV_addressbook.view_contact(contact_id)

@app.route('/contacts/add', methods=['GET', 'POST'])
@login_required
def add_contact_route():
    return OV_addressbook.add_contact()

@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def edit_contact_route(contact_id):
    return OV_addressbook.edit_contact(contact_id)

@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
@login_required
def delete_contact_route(contact_id):
    return OV_addressbook.delete_contact(contact_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5008, debug=True)
