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
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS catalog (
                id SERIAL PRIMARY KEY,
                date VARCHAR(250),
                photo1 VARCHAR(250),
                photo2 VARCHAR(250),
                photo3 VARCHAR(250),
                description VARCHAR(250),
                price VARCHAR(250)
            )''')
        conn.commit()
        cursor.close()


def get_catalog_data():
    """AI is creating summary for get_catalog_data

    Returns:
        [type]: [description]
    """
    with db_connect() as conn:
        cursor = conn.cursor()
# Execute a SELECT query to fetch all records from the 'catalog' table.
        cursor.execute("SELECT * FROM catalog")
# Retrieve all the results from the query.
        data = cursor.fetchall()
        cursor.close()
        return data


def insert_apartment_data(data):
    with db_connect() as conn:
        cursor = conn.cursor()
        # Use %s placeholders for parameterized queries in psycopg2.
        cursor.execute(
            """
            INSERT INTO catalog (date, photo1, photo2, photo3, description, price)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            data
        )
        # Commit the transaction
        conn.commit()
        cursor.close()