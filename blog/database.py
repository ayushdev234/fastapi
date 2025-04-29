from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


"""engine	How to connect to database
SessionLocal	Creates sessions (to make queries and transactions)
Base	Base class to define database models (tables)"""

SQLALCHEMY_DATABASE_URL = 'sqlite:///./blog.db'

# Use a single engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

# Keep only one get_db()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()