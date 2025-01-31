from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.schemas import BudgetResponse, BudgetCreate, BudgetUpdateRequest
from app.models import Budget, Expense
from app import crud
from db.database import get_db
from utils.auth import get_current_user_id

router = APIRouter()

@router.post("/", response_model=BudgetResponse)
def add_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # # Default month = current month if not provided 
    # if budget.month is None:
    #     budget.month = datetime.now().strftime("%Y-%m")

    # Check if budget for the category already exists
    existing_budget = (
        db.query(Budget)
        .filter(Budget.user_id == user_id, Budget.category == budget.category,Budget.month == budget.month)
        .first()
    )
    if existing_budget:
        raise HTTPException(status_code=400, detail=f"Budget for this category alreayd exists for {budget.month}. Please update the budget")
    
    budget = crud.create_budget(db=db, budget=budget, user_id=user_id)
    return budget


@router.get("/", response_model=list[BudgetResponse])
def get_user_budget(
    month: str = None,  # Optional query parameter for filtering by month 
    db: Session = Depends(get_db),
    user_id: id = Depends(get_current_user_id)
):
    budgets = crud.get_budget_by_user(db=db, user_id=user_id, month=month)
    if not budgets:
        raise HTTPException(status_code=404, detail="No Budget Found!")
    return budgets


@router.put("/update_budget", response_model=dict)
def update_budget(
    update_data: BudgetUpdateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # Find the budget by category and month
    budget = (
        db.query(Budget)
        .filter(
            Budget.user_id == user_id,
            Budget.category == update_data.category,
            Budget.month == update_data.month
        )
        .first()
    )
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found for the specified category or month.")

    # Update the budget limit
    warning = None
    if update_data.new_limit:
        if update_data.new_limit < budget.current_total:
            warning = (
                f"The new budget limit ({update_data.new_limit}) for '{update_data.category}' "
                f"is lower than your current spending ({budget.current_total}). "
                "You won't be able to add more expenses for this category until your spending is reduced. "
                "Consider increasing the budget or adjusting your expenses to stay within the new limit."
            )
        budget.limit = update_data.new_limit

    db.commit()
    db.refresh(budget)

    # Return the updated budget as a Pydantic object
    response = {"message": "Budget updated successfully"}
    if warning:
        response["warning"] = warning
    
    return response


@router.get("/budget-warnings", response_model=dict)
def check_budget_warnings(
    month: str = None,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if month is None:
        month = datetime.now().strftime("%Y-%m")

    # Get all budgets set by the user for the given month
    budgets = db.query(Budget).filter(
        Budget.user_id == user_id, Budget.month == month
    ).all()

    if not budgets:
        return {"message": "No budgets set for this month."}

    warnings = []

    for budget in budgets:
        # Get total expenses for the category
        total_spent = db.query(func.sum(Expense.amount)).filter(
            Expense.user_id == user_id,
            Expense.category == budget.category,
            func.to_char(Expense.date, 'YYYY-MM') == month
        ).scalar() or 0

        # Check if expenses exceed 80% of the budget limit
        if total_spent >= 0.8 * budget.limit:
            if total_spent >= budget.limit:
                warnings.append(
                    f"You have exceeded your '{budget.category}' budget for {month}. Consider adjusting your expenses."
                )
            else:
                warnings.append(
                    f"You have used {int((total_spent/budget.limit)*100)}% of your '{budget.category}' budget for {month}."
                )

    if warnings:
        return {"warnings": warnings}
    
    return {"message": "You are within your budget limits for this month."}