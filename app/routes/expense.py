from datetime import datetime
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app import crud
from app.models import Expense, Budget
from app.schemas import ExpenseCreate, ExpenseResponse
from db.database import get_db
from utils.auth import get_current_user_id

router = APIRouter()

# 1. Add expenses
@router.post("/", response_model=ExpenseResponse)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
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
            category=expense.category,
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
