from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DATABASE_URL = 'posgresql://<username>:<password>@<ip_address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'posgresql://<username>:<password>@<postgresserver>/<database_name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

# engine is responsible for establishing connection to sql postgres database, however for talking with sql database you need session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# creating session for communicating with database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()  # for creating tables

# Dependency


def get_db():  # definiramo funkciju koju ćemo svaki puta kada dobijemo neki request pozvati pvezati sa sa bazom podataka, napravitit ćemo session (komunikaciju sa bazom - slat cemo SQL naredbe) i kada je taj request gotov  samo zatvorimo bazu
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     # every time u are using sth that can fail (like database) you should us e python try statement to se if it will establish connection
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastAPI_database', user='postgres', password='archer22pilot',
#                                 cursor_factory=RealDictCursor)  # psycopg.connect(host, database, user, password)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connectong to database failed!!")
#         print("Error: ", error)
#         time.sleep(2)
