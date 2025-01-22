from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import List, Optional
from datetime import datetime, date

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

    @field_validator("amount")
    def validate_amount(cls, value):
        if value <= 0:
            raise ValueError("Expense amount must be greater than zero.")
        return value
    
    @field_validator("date")
    def validate_date(cls, value):
        if value > date.today():
            raise ValueError("Expense date cannot be in the future.")
        return value

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
    month: Optional[str] = Field(None, description="Month in YYYY-MM format")

    @field_validator("category")
    def validate_category(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string.")
        return value
    
    @field_validator("limit")
    def validate_limit(cls, value):
        if value <= 0:
            raise ValueError("Budget limit must be greater than zero.")
        return value

    @field_validator("month")
    def validate_month(cls, value):
        if value is None:
            return value
        if not isinstance(value, str):
            raise TypeError("Month must be string in YYYY-MM format or none.")
        try:
            datetime.strptime(value, "%Y-%m")
            return value
        except ValueError:
            raise ValueError("Invalid month format. Use YYYY-MM.")

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

class BudgetUpdateRequest(BaseModel):
    category: str
    month: str = Field(..., description="Month in YYYY-MM format")
    new_limit: float = Field(..., description="The updated budget limit (must be greater than zero)")

    @field_validator("category")
    def validate_category(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string.")
        return value

    @field_validator("month")
    def validate_month(cls, value):
        try:
            datetime.strptime(value, "%Y-%m")
            return value
        except ValueError:
            raise ValueError("Invalid month format. Use YYYY-MM.")

    @field_validator("new_limit")
    def validate_new_limit(cls, value):
        if value <= 0:
            raise ValueError("Budget limit must be greater than zero.")
        return value