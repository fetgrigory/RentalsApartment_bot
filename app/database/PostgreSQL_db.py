'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/10/2024
Ending //
'''
import psycopg2
import os

def db_connect():
    """AI is creating summary for db_connect

    Returns:
        [type]: [description]
    """
    # Establish a connection to the PostgreSQL database using environment variables
    return psycopg2.connect(
        # Database host
        host=os.getenv('HOST'),
        # Name of the database
        dbname=os.getenv('DBNAME'),
        # Username for authentication
        user=os.getenv('USER'),
        # Password for authentication
        password=os.getenv('PASSWORD'),
        # Port number for database connection
        port=os.getenv('PORT')
    )

def create_database():
    """AI is creating summary for create_database
    """    
    with db_connect() as conn:
        cursor = conn.cursor()
        # Create the 'catalog' table if it does not exist, defining its structure.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS catalog (
                id SERIAL PRIMARY KEY,
                date VARCHAR(250),
                photo1 VARCHAR(250),
                photo2 VARCHAR(250),
                photo3 VARCHAR(250),
                description VARCHAR(250),
                address VARCHAR(250),
                price VARCHAR(250),
                category VARCHAR(250)
            )
        ''')
        conn.commit()

def get_catalog_data():
    """AI is creating summary for get_catalog_data

    Returns:
        [type]: [description]
    """    
    with db_connect() as conn:
        cursor = conn.cursor()
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
        cursor.execute("SELECT * FROM catalog WHERE category = %s", (category,))
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
        cursor.execute(
            "INSERT INTO catalog (date, photo1, photo2, photo3, description, address, price, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            data
        )
        conn.commit()

def delete_apartment_data(apartment_id):
    """AI is creating summary for delete_apartment_data

    Args:
        apartment_id ([type]): [description]
    """    
    with db_connect() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM catalog WHERE id = %s", (apartment_id,))
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
            "UPDATE catalog SET photo1=%s, photo2=%s, photo3=%s, description=%s, address=%s, price=%s, category=%s WHERE id=%s",
            (photo1, photo2, photo3, description, address, price, category, apartment_id)
        )
        conn.commit()