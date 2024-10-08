'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
import sqlite3


def db_connect():
    """AI is creating summary for db_connect

    Returns:
        [type]: [description]
    """

    # The function returns a connection object to the 'catalog.db' database.
    return sqlite3.connect('catalog.db')


def create_database():
    """AI is creating summary for create_database
    """
    with db_connect() as conn:
        cursor = conn.cursor()
# Create the 'catalog' table if it does not exist, defining its structure.
    cursor.execute('''CREATE TABLE IF NOT EXISTS catalog
                   (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date VARCHAR(50),
                   photo1 VARCHAR(50),
                   photo2 VARCHAR(50),
                   photo3 VARCHAR(50),
                   description VARCHAR(50),
                   price VARCHAR(50))''')
    conn.commit()
    conn.close()


def get_catalog_data():
    """AI is creating summary for get_catalog_data
    """
    with db_connect() as conn:
        cursor = conn.cursor()
# Execute a SELECT query to fetch all records from the 'catalog' table.
    cursor.execute("SELECT * FROM catalog")
# Retrieve all the results from the query.
    data = cursor.fetchall()
    conn.close()
    return data


def insert_apartment_data(data):
    """AI is creating summary for insert_apartment_data

    Args:
        data ([type]): [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
# Insert a new record into the 'catalog' table using the provided data.
    cursor.execute("INSERT INTO catalog (date, photo1, photo2, photo3, description, price) VALUES (?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    conn.close()
