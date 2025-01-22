from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import BudgetResponse, BudgetCreate
from app.models import Budget
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
    # Check if budget for the category already exists
    existing_budget = (
        db.query(Budget)
        .filter(Budget.user_id == user_id, Budget.category == budget.category)
        .first()
    )
    if existing_budget:
        raise HTTPException(status_code=400, detail="Budget for this category alreayd exists. Please update the budget")
    
    return crud.create_budget(db=db, budget=budget, user_id=user_id)

@router.get("/", response_model=list[BudgetResponse])
def get_user_budget(
    db: Session = Depends(get_db),
    user_id: id = Depends(get_current_user_id)
):
    budgets = crud.get_budget_by_user(db=db, user_id=user_id)
    if not budgets:
        raise HTTPException(status_code=404, detail="No Budget Found!")
    return budgets