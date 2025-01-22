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
@router.post("/", response_model=dict)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    try:
        # Determine the month of the expense
        current_month = expense.date.month
        current_year = expense.date.year

        # Check if a budget exists for the category
        budget = (
            db.query(Budget)
            .filter(Budget.category == expense.category, Budget.user_id == user_id)
            .first()
        )
        if budget:
            # Check if the expense month matches the current budget's month
            last_expense = (
                db.query(Expense)
                .filter(Expense.category == expense.category, Expense.user_id == user_id)
                .order_by(Expense.date.desc())
                .first()
            )
            if last_expense:
                last_month = last_expense.date.month
                last_year = last_expense.date.year
                if last_month != current_month or last_year != current_year:
                    # If the month has changed, reset current_total for the previous month
                    budget.current_total = 0.0
            
            # Check if adding the expense exceeds the budget limit
            if budget.current_total + expense.amount > budget.limit:
                raise HTTPException(
                    status_code=400, 
                    detail=(
                        f"Adding this expense exceeds you budget for {expense.category}. "
                        f"Current total: {budget.current_total}, Limit: {budget.limit}"
                    ),
                )
        # Add the expense
        new_expense = Expense(
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
            user_id=user_id,
        )
        db.add(new_expense)

        # Update the budget's current total
        if budget:
            budget.current_total += expense.amount
        
        db.commit()
        return {"message": "Expense added successfully"}
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
