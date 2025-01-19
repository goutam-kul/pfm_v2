from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Integer auto-increment ID
    username = Column(String, nullable=False, unique=True)  
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("Budget", back_populates="user")

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Unique ID for each expense
    category = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to User
    user = relationship("User", back_populates="expenses")


class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category = Column(String, nullable=False)
    limit = Column(Float, nullable=False)
    current_total = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to User
    user = relationship("User", back_populates="budgets")
