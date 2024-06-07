from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define Base
Base = declarative_base()

# Define your models
class SomeModel(Base):
    __tablename__ = 'some_table'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Add more columns as needed

# Create engine and session
engine = create_engine('sqlite:///budgetapp.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables in the database
Base.metadata.create_all(engine)

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



class User:
    def __init__(self, name, initial_balance=0):
        self.name = name
        self.balance = initial_balance
        self.transactions = []

    def add_transaction(self, amount, category):
        self.balance += amount
        self.transactions.append({"amount": amount, "category": category})

    def get_statement(self):
        return self.transactions

    def analyze_spending(self):
        analysis = {}
        for transaction in self.transactions:
            if transaction["category"] not in analysis:
                analysis[transaction["category"]] = 0
            analysis[transaction["category"]] += transaction["amount"]
        return analysis

class Transaction:
    def __init__(self, user, amount, category):
        self.user = user
        self.amount = amount
        self.category = category

    def get_details(self):
        return {"User": self.user, "Amount": self.amount, "Category": self.category}




class Category:
    def __init__(self, name):
        self.name = name
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

    def get_total_spent(self):
        total = 0
        for transaction in self.transactions:
            total += transaction.amount
        return total




class Goal:
    def __init__(self, category, amount):
        self.category = category
        self.amount = amount
        self.progress = 0

    def add_progress(self, amount):
        self.progress += amount

    def get_progress(self):
        return self.progress

    def is_goal_met(self):
        return self.progress >= self.amount






















# COMMAND LINE INTERFACE


import argparse

def main():
    parser = argparse.ArgumentParser(description="CLI for our finance tracking application")
    
    subparsers = parser.add_subparsers(dest="command")

    # Add parsers for each command
    user_parser = subparsers.add_parser("user", help="User related commands")
    user_parser.add_argument("--name", help="The name of the user")

    transaction_parser = subparsers.add_parser("transaction", help="Transaction related commands")
    transaction_parser.add_argument("--user", help="The user making the transaction")
    transaction_parser.add_argument("--amount", type=float, help="The amount of the transaction")
    transaction_parser.add_argument("--category", help="The category of the transaction")

    category_parser = subparsers.add_parser("category", help="Category related commands")
    category_parser.add_argument("--name", help="The name of the category")

    goal_parser = subparsers.add_parser("goal", help="Goal related commands")
    goal_parser.add_argument("--category", help="The category of the goal")
    goal_parser.add_argument("--amount", type=float, help="The amount of the goal")

    args = parser.parse_args()

    # Handle each command
    if args.command == "user":
        handle_user_command(args)
    elif args.command == "transaction":
        handle_transaction_command(args)
    elif args.command == "category":
        handle_category_command(args)
    elif args.command == "goal":
        handle_goal_command(args)

def handle_user_command(args):
    # TODO: Implement user command handling
    pass

def handle_transaction_command(args):
    # TODO: Implement transaction command handling
    pass

def handle_category_command(args):
    # TODO: Implement category command handling
    pass

def handle_goal_command(args):
    # TODO: Implement goal command handling
    pass

if __name__ == "__main__":
    main()














