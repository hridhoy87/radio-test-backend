# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Use psycopg3 connection string format
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_DhnsvcXJ0QL7@ep-soft-sky-ad2pszds-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require")


engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True, 
    pool_recycle=300)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()