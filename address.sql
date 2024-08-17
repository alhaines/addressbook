# Check if users table exists, if not, create it
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);
""")

# Check if addresses table exists, if not, create it
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
