from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define User, Expense, and Balance models
class User(Base):
    _tablename_ = 'users'

    user_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    mobile = Column(String)

    expenses = relationship("Expense", back_populates="payer")
    balances = relationship("Balance", back_populates="user")

class Expense(Base):
    _tablename_ = 'expenses'

    expense_id = Column(String, primary_key=True)
    payer_id = Column(String, ForeignKey('users.user_id'))
    amount = Column(Float)
    expense_type = Column(String)
    expense_name = Column(String)
    notes = Column(String)
    images = Column(String)

    payer = relationship("User", back_populates="expenses")

class Balance(Base):
    _tablename_ = 'balances'

    balance_id = Column(Integer, primary_key=True, autoincrement=True)
    debtor_id = Column(String, ForeignKey('users.user_id'))
    creditor_id = Column(String, ForeignKey('users.user_id'))
    amount = Column(Float)

    user = relationship("User", back_populates="balances")

# Create a SQLite database
engine = create_engine('sqlite:///expense.db')

# Create tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Example usage to add data to the database
if _name_ == "_main_":
    # Add users
    user1 = User(user_id="u1", name="User1", email="user1@example.com", mobile="1234567890")
    user2 = User(user_id="u2", name="User2", email="user2@example.com", mobile="9876543210")
    user3 = User(user_id="u3", name="User3", email="user3@example.com", mobile="5555555555")

    session.add_all([user1, user2, user3])
    session.commit()

    # Add expenses
    expense1 = Expense(expense_id="e1", payer=user1, amount=1000, expense_type="EQUAL", expense_name="Electricity Bill")
    expense2 = Expense(expense_id="e2", payer=user1, amount=1250, expense_type="EXACT", expense_name="Flipkart Sale")

    session.add_all([expense1, expense2])
    session.commit()

    # Add balances (you can add balances as expenses are added)
    # Example: balance1 = Balance(debtor=user2, creditor=user1, amount=370)
    # session.add(balance1)
    # session.commit()
    
    # Query and manipulate data as needed using session.query

    # Close the session when done
    session.close()