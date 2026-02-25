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
# Loading variables from .env
load_dotenv()
# Getting variables from the environment
HOST = os.getenv("HOST")
DBNAME = os.getenv("DBNAME")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
PORT = os.getenv("PORT")
# Creating a connection string
DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
# Creating an engine
sync_engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)
# Session factory
session_factory = sessionmaker(
    bind=sync_engine,
    autoflush=False,
    autocommit=False

)
