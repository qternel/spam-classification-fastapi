import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

pwd = os.getenv("DB_PASSWORD")

DB_URL = f"postgresql+psycopg://postgres:{pwd}@db:5432/app_db"
connect_args = {}

engine = create_engine(DB_URL, connect_args=connect_args)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
