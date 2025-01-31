import random
import string
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from app import crud, schemas
from db.database import get_db
from utils.password_utils import generate_password_hash, verify_password
from utils.email_utils import send_reset_email
import uuid
from utils.auth import create_access_token, get_current_user_id
from datetime import timedelta, datetime, timezone


ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Expiration time for auth token

router = APIRouter()

def validate_password_strength(password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long."
        )

# 1. Register a new User
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Validate password strength
    validate_password_strength(user.password)

    # Check if the email or usename is already registered. 
    if crud.get_user_by_email(db=db, email=user.email) or crud.get_user_by_username(db=db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error 400: Email or Username is already registered."
        )
    
    # Hash the password
    hashed_password = generate_password_hash(user.password)

    # Create the user
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

# 2. Login existing user
@router.post("/login", response_model=schemas.LoginResponse)
def login_user(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Extract identifier and password from the request body
    identifier = request.identifier
    password = request.password

    # Search user by email and username
    user = crud.get_user_by_email(db=db, email=identifier) or crud.get_user_by_username(db=db, username=identifier)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error: User Not Found"
        )
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid Password")
    
    # Generate access token
    access_token = create_access_token(
        data={"user_id": user.id},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # Return the token
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# 3. Forgot password email send 
@router.post("/forgot-password")
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = request.email
    # Check if the email exists
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Email not registered"
        )
    
    # # Generate a secure reset token
    # reset_token = str(uuid.uuid4())
    # user.reset_token = reset_token  # Store token in the database
    # db.commit()

    # # Generate reset link
    # reset_link = f"http://yourdomain.com/reset-password?token={reset_token}"

    # Generate a 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))
    otp_expiry = datetime.now(timezone.utc) + timedelta(minutes=10) # OTP expires in 10 minutes

    # Store OTP and expiry in database
    user.reset_otp = otp
    user.otp_expiry = otp_expiry
    db.commit()
    email_subject = "Your Password Reset OTP"
    email_body = f"Your OTP for password reset is {otp}. It will expire in 10 minutes."
    await send_reset_email(to_email=email, email_body=email_body, email_subject=email_subject)

    return {"message": "An OTP has been sent to your email."}

# 4. Reset password
@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    # Extract token and new password from the request
    # token = request.token
    otp = request.otp
    new_password = request.new_password

    # Validate new password
    validate_password_strength(new_password)

    # Verify OTP and fetch user
    user = crud.get_user_by_otp(db=db, otp=otp)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token."
        )
    
    # Hash the new password
    hashed_password = generate_password_hash(new_password)
    # Update the user's password in the database
    user.hashed_password = hashed_password
    db.commit()

    return {"message": "Your password has been reset successfully."}


@router.get("/user_id")
def get_user_id(
    authorization: str = Header(...),  # Extract the Authorization header
    db: Session = Depends(get_db)
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid token format")
    
    # Extrac the token from the header
    access_token = authorization.split(" ")[1]

    user_id = get_current_user_id(access_token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"user_id": user_id}


# Income endpoints 

@router.put("/income", response_model=schemas.UpdateIncomeRequest)
def update_income(
    update_data: schemas.UpdateIncomeRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # Find the income of the user
    update_income = crud.get_user(db=db, user_id=user_id)

    # Check if the user exists
    if not update_income:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's income with the new value
    update_income.monthly_income = update_data.monthly_income

    db.commit()
    db.refresh(update_income)  # Updates the income object with new data
    
    return {"message": "Income updated successfully", "monthly_income": update_income.monthly_income}


@router.get("/income")
def get_income(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    income = crud.get_user(db=db, user_id=user_id)
    return {"monthly_income": income.monthly_income}


