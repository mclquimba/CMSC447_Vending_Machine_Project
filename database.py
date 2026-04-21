import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db = os.getenv('DB')
driver = os.getenv('DB_DRIVER')
username = os.getenv('DB_USERNAME')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
name = os.getenv('DB_NAME')

db_url = f"{db}+{driver}://{username}:{password}@{host}:{port}/{name}"

engine = create_engine(db_url, echo=True)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)