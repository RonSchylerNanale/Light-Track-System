
from subprocess import call
import subprocess
import mysql.connector

def open_signup():
    subprocess.Popen(['python', 'lib/logindb.py'])

def create_tables():
    # Connect to MySQL
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LTS",
        port = 3306
    )
    cursor = mydb.cursor()

    # Define SQL queries for creating tables
    create_table_users = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username VARCHAR(45) NOT NULL,
            password VARCHAR(45) NOT NULL
        )
    """

    create_table_change_log = """
        CREATE TABLE IF NOT EXISTS change_log (
            id INT AUTO_INCREMENT PRIMARY KEY,
            action VARCHAR(50) NOT NULL,
            registration_number INT NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """

    create_table_products = """
        CREATE TABLE IF NOT EXISTS products (
            registration INTEGER PRIMARY KEY,
            name VARCHAR(45) NOT NULL,
            category VARCHAR(45) NOT NULL,
            description VARCHAR(255) NOT NULL, 
            date DATE NOT NULL, 
            price INTEGER NOT NULL, 
            quantity INTEGER NOT NULL, 
            attributes VARCHAR(255) NOT NULL, 
            supplier VARCHAR(255) NOT NULL,
            image LONGBLOB 
        )
    """

    create_table_archive = """
        CREATE TABLE IF NOT EXISTS archive (
            registration VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            category VARCHAR(255),
            description TEXT,
            date DATE,
            price DECIMAL(10, 2),
            quantity INT,
            attributes TEXT,
            supplier VARCHAR(255),
            image LONGBLOB
        )
    """
    create_table_order_log = """
        CREATE TABLE IF NOT EXISTS order_log (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            registration_number VARCHAR(255),
            product_name VARCHAR(255),
            amount_sold INT,
            price DECIMAL(10, 2),
            total_price DECIMAL(10, 2),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """

    # Execute SQL queries
    cursor.execute(create_table_users)
    cursor.execute(create_table_change_log)
    cursor.execute(create_table_products)
    cursor.execute(create_table_archive)
    cursor.execute(create_table_order_log)


    # Commit changes and close connection
    mydb.commit()
    cursor.close()
    mydb.close()

if __name__ == "__main__":
    create_tables()

open_signup()
