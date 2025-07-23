# A Simple, Secure Address Book (Flask Edition) v2.0

This is a simple, clean, and secure web-based address book application built with Python and the Flask web framework. It allows multiple users to register, log in, and manage their own private list of contacts.

This project is a complete refactoring of an earlier version, rebuilt from the ground up to use modern, modular, and secure coding practices.

## Features

-   **Multi-User Support:** Each user has a separate, secure login and can only see and manage their own contacts.
-   **Secure Password Storage:** User passwords are not stored in plaintext. They are securely hashed using modern cryptographic standards (`werkzeug.security`).
-   **Full CRUD Functionality:** Users can **C**reate, **R**ead, **U**pdate, and **D**elete their contacts through a clean web interface.
-   **Modular, Robust Backend:** The application is built on a modular design, separating the web routes (in `app.py`) from the application logic (in `OV_addressbook.py`).
-   **Centralized Database Management:** Uses a global `MySql.py` module for all database connections, preventing common errors like "MySQL has gone away."

## Requirements

1.  A Linux system with Python 3 and `pip`.
2.  A working MySQL/MariaDB server.
3.  The `werkzeug` and `flask` Python libraries (installation is handled by the installer).

## Installation

1.  Download or clone this project to a directory on your server (e.g., `~/projects/AddressBook_v2`).
2.  Navigate into the project directory: `cd ~/projects/AddressBook_v2`
3.  **Database Setup:** Before running the app, you must create the database and tables. An SQL script is provided to do this automatically.
    *   First, create a new, empty database (e.g., `addressbook`) in your MySQL server.
    *   Then, update the `config.py` file with the correct database name and your credentials.
    *   Ensure that /home/$USER/.my.cnf contains you MySql credentials.
    *   Finally, import the provided schema file:
        ```bash
        mysql --defaults-file=/home/$USER/.my.cnf addressbook < addressbook_schema_v2.sql
        ```
4.  **Install Python Dependencies:** A `requirements.txt` file is included. Install the necessary libraries with pip:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file containing `Flask`, `PyMySQL`, and `Werkzeug`)*

## Running the Application

### For Development / Testing:

You can run the application directly using Python. This will start the built-in Flask development server.

```bash
cd ~/projects/AddressBook_v2
python3 ./app.py
