from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
# from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from src.database.db import engine

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    # id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False, index=True)
    lastname = Column(String(50), index=True)
    email = Column(String(40), unique=True, index=True)
    phone = Column(String(50), index=True)
    birthdate = Column('birth', Date)
    otherinform = Column(String(150), nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="contacts")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
  
Base.metadata.create_all(bind=engine)


    