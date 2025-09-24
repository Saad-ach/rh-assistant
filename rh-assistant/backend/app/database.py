from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Use DATABASE_URL from settings, or fallback to a file-based SQLite database for development stability
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL if settings.DATABASE_URL else "sqlite:///./app.db"

# For SQLite, connect_args are needed to allow multiple threads to interact with the database
# For other databases like PostgreSQL, these arguments are not necessary.
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 