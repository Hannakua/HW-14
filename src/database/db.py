from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.conf.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/contactsdb"
# docker run --name rest_app -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

# SQLALCHEMY_DATABASE_URL = "sqlite:///mycontacts.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

  
