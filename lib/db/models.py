from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    transactions = relationship('Transaction', back_populates='user')
    goals = relationship('Goal', back_populates='user')

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    date = Column(Date)
    description = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user = relationship('User', back_populates='transactions')
    category = relationship('Category', back_populates='transactions')

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    transactions = relationship('Transaction', back_populates='category')

class Goal(Base):
    __tablename__ = 'goals'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Float)
    description = Column(String)
    user = relationship('User', back_populates='goals')
