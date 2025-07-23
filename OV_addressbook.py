#
# filename:   /home/al/projects/AddressBook_v2/OV_addressbook.py
#
# v1.1: Adds the 'view_contact' function to display full contact details.

from flask import render_template, request, redirect, session, url_for, flash
from MySql import MySQL
import config

db = MySQL(**config.mysql_config)

# --- NEW: Function to view a single contact ---
def view_contact(contact_id):
    """Fetches a single contact and displays its full details."""
    user_id = session.get('user_id')
    contact = db.get_data("SELECT * FROM contacts WHERE id = %s AND owner_id = %s", (contact_id, user_id))

    if contact:
        return render_template('view_contact.html', contact=contact[0])
    else:
        flash("Contact not found or you do not have permission to view it.", "error")
        return redirect(url_for('list_contacts_route'))

# --- Other functions are unchanged ---
def list_contacts():
    user_id = session.get('user_id')
    contacts = db.get_data("SELECT * FROM contacts WHERE owner_id = %s ORDER BY lastname, firstname ASC", (user_id,))
    return render_template('list_contacts.html', contacts=contacts)

def add_contact():
    if request.method == 'POST':
        owner_id = session.get('user_id')
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        comment = request.form.get('comment')
        query = """
            INSERT INTO contacts (owner_id, firstname, lastname, address, city, state, zipcode, birthday, email, phone1, phone2, comment)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (owner_id, firstname, lastname, address, city, state, zipcode, birthday, email, phone1, phone2, comment)
        if db.put_data(query, params):
            flash(f"Contact '{firstname} {lastname}' added successfully!", 'success')
        else:
            flash("Failed to add contact.", 'error')
        return redirect(url_for('list_contacts_route'))
    return render_template('contact_form.html', form_title="Add New Contact", contact={})

def edit_contact(contact_id):
    user_id = session.get('user_id')
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')
        birthday = request.form.get('birthday')
        email = request.form.get('email')
        phone1 = request.form.get('phone1')
        phone2 = request.form.get('phone2')
        comment = request.form.get('comment')
        query = """
            UPDATE contacts SET firstname=%s, lastname=%s, address=%s, city=%s, state=%s,
            zipcode=%s, birthday=%s, email=%s, phone1=%s, phone2=%s, comment=%s
            WHERE id=%s AND owner_id=%s
        """
        params = (firstname, lastname, address, city, state, zipcode, birthday, email, phone1, phone2, comment, contact_id, user_id)
        if db.put_data(query, params):
            flash(f"Contact '{firstname} {lastname}' updated successfully!", 'success')
        else:
            flash("Failed to update contact.", 'error')
        return redirect(url_for('list_contacts_route'))
    contact_data = db.get_data("SELECT * FROM contacts WHERE id = %s AND owner_id = %s", (contact_id, user_id))
    if contact_data:
        return render_template('contact_form.html', form_title="Edit Contact", contact=contact_data[0])
    else:
        flash("Contact not found or you do not have permission to edit it.", "error")
        return redirect(url_for('list_contacts_route'))

def delete_contact(contact_id):
    user_id = session.get('user_id')
    contact_data = db.get_data("SELECT firstname, lastname FROM contacts WHERE id = %s AND owner_id = %s", (contact_id, user_id))
    if contact_data:
        if db.put_data("DELETE FROM contacts WHERE id = %s", (contact_id,)):
            flash(f"Contact '{contact_data[0]['firstname']} {contact_data[0]['lastname']}' deleted successfully.", 'success')
        else:
            flash("Failed to delete contact.", 'error')
    else:
        flash("Contact not found or you do not have permission to delete it.", "error")
    return redirect(url_for('list_contacts_route'))
