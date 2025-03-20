'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2024
Ending //

'''
import sqlite3
import datetime


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
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER UNIQUE,
                          first_name VARCHAR(50),
                          last_name VARCHAR(50),
                          phone VARCHAR(50))''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS bookings
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          user_id INTEGER,
                          apartment_id INTEGER,
                          start_date DATE,
                          end_date DATE,
                          rent_days INTEGER,
                          total_price INTEGER,
                          FOREIGN KEY (user_id) REFERENCES users(user_id),
                          FOREIGN KEY (apartment_id) REFERENCES catalog(id))''')
        conn.commit()


# Check if there is a user in the database
def check_user_exists(user_id):
    """AI is creating summary for check_user_exists

    Args:
        user_id ([type]): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone() is not None


# Adding the user to the database
def insert_user_data(user_id, first_name, last_name, phone):
    """AI is creating summary for insert_user_data

    Args:
        user_id ([type]): [description]
        first_name ([type]): [description]
        last_name ([type]): [description]
        phone ([type]): [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        if check_user_exists(user_id):
            cursor.execute(
                "UPDATE users SET first_name=?, last_name=?, phone=? WHERE user_id=?",
                (first_name, last_name, phone, user_id)
            )
        else:
            cursor.execute(
                "INSERT INTO users (user_id, first_name, last_name, phone) VALUES (?, ?, ?, ?)",
                (user_id, first_name, last_name, phone)
            )
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
        # Executing SQL query to retrieve all items from the catalog for the given category
        cursor.execute("SELECT * FROM catalog WHERE category = ?", (category,))
        data = cursor.fetchall()
    return data


# Checking if the apartment is available
def is_apartment_available(apartment_id, start_date, end_date):
    """AI is creating summary for is_apartment_available

    Args:
        apartment_id ([type]): [description]
        start_date ([type]): [description]
        end_date ([type]): [description]

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM bookings
            WHERE apartment_id = ?
            AND ((start_date <= ? AND end_date >= ?)
            OR (start_date <= ? AND end_date >= ?))
        """, (apartment_id, start_date, start_date, end_date, end_date))
        return cursor.fetchone() is None


# Inserts a new booking record
def insert_booking_data(user_id, apartment_id, start_date, rent_days, total_price):
    """AI is creating summary for insert_booking_data

    Args:
        user_id ([type]): [description]
        apartment_id ([type]): [description]
        start_date ([type]): [description]
        rent_days ([type]): [description]
        total_price ([type]): [description]
    """    
    with db_connect() as conn:
        cursor = conn.cursor()
        end_date = start_date + datetime.timedelta(days=rent_days)
        cursor.execute(
            "INSERT INTO bookings (user_id, apartment_id, start_date, end_date, rent_days, total_price) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, apartment_id, start_date, end_date, rent_days, total_price)
        )
        conn.commit()


# Retrieves all booking records along with user and apartment details.
def get_bookings():
    """AI is creating summary for get_bookings

    Returns:
        [type]: [description]
    """    
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT bookings.id, users.first_name, users.last_name, catalog.address, bookings.start_date, bookings.end_date, bookings.rent_days, bookings.total_price
            FROM bookings
            JOIN users ON bookings.user_id = users.user_id
            JOIN catalog ON bookings.apartment_id = catalog.id
        """)
        return cursor.fetchall()


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
