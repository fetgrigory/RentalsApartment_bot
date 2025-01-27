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
                          address VARCHAR(50),
                          price VARCHAR(50),
                          category VARCHAR(50))''')
        conn.commit()


def get_catalog_data():
    """AI is creating summary for get_catalog_data
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        # Execute a SELECT query to fetch all records from the 'catalog' table.
        cursor.execute("SELECT * FROM catalog")
        # Retrieve all the results from the query.
        data = cursor.fetchall()
    return data


def get_catalog_by_category(category):
    """AI is creating summary for get_catalog_by_category

    Args:
        category ([type]): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM catalog WHERE category = ?", (category,))
        data = cursor.fetchall()
    return data


def insert_apartment_data(data):
    """AI is creating summary for insert_apartment_data

    Args:
        data ([type]): [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        # Insert a new record into the 'catalog' table using the provided data.
        cursor.execute("INSERT INTO catalog (date, photo1, photo2, photo3, description, address, price, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
        conn.commit()


def delete_apartment_data(apartment_id):
    """AI is creating summary for delete_apartment_data

    Args:
        apartment_id ([type]): [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM catalog WHERE id = ?", (apartment_id,))
        conn.commit()


def update_apartment_data(apartment_id, photo1, photo2, photo3, description, address, price, category):
    """AI is creating summary for update_apartment_data

    Args:
        apartment_id ([type]): [description]
        photo1 ([type]): [description]
        photo2 ([type]): [description]
        photo3 ([type]): [description]
        description ([type]): [description]
        address ([type]): [description]
        price ([type]): [description]
        category ([type]): [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE catalog SET photo1=?, photo2=?, photo3=?, description=?, address=?, price=?, category=? WHERE id=?",
            (photo1, photo2, photo3, description, address, price, category, apartment_id)
        )
        conn.commit()
