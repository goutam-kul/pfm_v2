from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

# 1. User Schema 
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str 

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True  # Enables ORM compatibility 

# Login User
class LoginRequest(BaseModel):
    identifier: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str

# Forgot password
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# Reset Password
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

# ------------------------------------------------

# 2. Expense Schema
class ExpenseBase(BaseModel):
    category: str
    amount: float
    date: date

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

#------------------------------------------------

# 3. Budget Schema
class BudgetBase(BaseModel):
    category: str
    limit: float
    current_total: float = 0.0

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True