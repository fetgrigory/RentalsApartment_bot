'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 10/01/2026
Ending //

'''
# Installing the necessary libraries
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.models import Base
# Loading variables from .env
load_dotenv()
# Getting variables from the environment
HOST = os.getenv("HOST")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
# Creating a connection string
DATABASE_URL = f"asyncpg+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
# Creating an engine
async_engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)
# Session factory
session_factory = sessionmaker(
    bind=async_engine,
    autoflush=False,
    autocommit=False

)


# Creates all tables if they do not exist
def init_db():
    """AI is creating summary for init_db
    """
    Base.metadata.create_all(bind=async_engine)
