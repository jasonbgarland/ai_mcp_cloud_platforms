import os

from models import Base
from sqlalchemy import create_engine

DB_USER = os.getenv("POSTGRES_USER", "itadmin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password1234")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "demo_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def reset_database():
    engine = create_engine(DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Database schema reset and initialized.")

if __name__ == "__main__":
    reset_database()
