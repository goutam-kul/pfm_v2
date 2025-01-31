from datetime import datetime
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, extract
from app import crud
from app.models import Expense, Budget
from app.schemas import ExpenseCreate, ExpenseResponse
from db.database import get_db
from utils.auth import get_current_user_id
from utils.category_mapper import standardize_category

router = APIRouter()

# 1. Add expenses
@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        # Standardize categories
        primary_category, subcategory = standardize_category(expense.category)

        if not primary_category:
            raise HTTPException(
                status_code=400, 
                detail=f"Unknown category: '{expense.category}'. Please use a valid category for your expense."
            )
        
        # Determine the month of the expense in YYYY-MM format
        expense_month = expense.date.strftime("%Y-%m")

        # Find the matching budget for the category and month
        budget = (
            db.query(Budget)
            .filter(
                Budget.category == expense.category,
                Budget.user_id == user_id,
                Budget.month == expense_month  # Match the month
            )
            .first()
        )

        # Add the expense
        new_expense = Expense(
            amount=expense.amount,
            category=primary_category,   # Store standardize primary category
            subcategory=subcategory,     # Store subcategory if available 
            date=expense.date,  # Keep full YYYY-MM-DD format
            user_id=user_id,
        )
        db.add(new_expense)

        # If a budget exists, update its current total
        if budget:
            if budget.current_total + expense.amount > budget.limit:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Adding this amount: {expense.amount} exceeds your budget for {expense.category}. "
                        f"Current usage: {budget.current_total} out of {budget.limit}. "
                        f"To stay within your budget, reduce the expense by {expense.amount - (budget.limit - budget.current_total)}."
                    ),
                )
            budget.current_total += expense.amount

        db.commit()
        return new_expense
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# 2. Show expenses
@router.get("/", response_model=list[ExpenseResponse])
def get_user_expenses(
    db: Session = Depends(get_db),  # Ensure this is clearly marked as a dependency
    user_id: int = Depends(get_current_user_id)  # Get user_id from the token
):
    expenses = crud.get_expenses_by_user(db=db, user_id=user_id)
    if not expenses:
        raise HTTPException(status_code=404, detail="No Expense found")
    return expenses



# Savinga endpoint

@router.get("/savings", response_model=dict)
def calculate_saving(
    month: str = None,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Get user's income
    user = crud.get_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # If month is not provided, use the current month (format: YYYY-MM)
    if month is None:
        month = datetime.now().strftime("%Y-%m")

    # Extract year and month from the given month string
    year, month_number = map(int, month.split("-"))

    # Query total expenses for the given month
    total_expenses = (
        db.query(func.sum(Expense.amount))
        .filter(
            Expense.user_id == user_id,
            extract("year", Expense.date) == year,   # Extract year from date column
            extract("month", Expense.date) == month_number  # Extract month from date column
        )
        .scalar() or 0
    )

    # Calculate savings
    savings = float(user.monthly_income) - float(total_expenses)

    return {
        "month": month,
        "income": user.monthly_income,
        "total_expenses": total_expenses,
        "savings": savings
    }