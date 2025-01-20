from sqlalchemy.orm import Session
from app import models, schemas

# User CRUD Operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.reset_token == token).first()

def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Expense CRUD Operations
def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: int):
    db_expense = models.Expense(**expense.model_dump(), user_id=user_id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses_by_user(db: Session, user_id: int):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).all()

# Budget CRUD Operations
def create_budget(db: Session, budget: schemas.BudgetCreate, user_id: int):
    db_budget = models.Budget(**budget.model_dump(), user_id=user_id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budget_by_user(db: Session, user_id: int):
    return db.query(models.Budget).filter(models.Budget.user_id == user_id).all()

    