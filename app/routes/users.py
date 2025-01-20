from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from db.database import get_db
from utils.password_utils import generate_password_hash, verify_password
from utils.email_utils import send_reset_email
import uuid

router = APIRouter()

# 1. Register a new User
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db=db, email=user.email) or crud.get_user_by_username(db=db, username=user.username):
        raise HTTPException(status_code=400, detail="Error 400: Email or Username is already registered.")
    
    # Hash the password
    hashed_password = generate_password_hash(user.password)

    # Create the user
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)

# 2. Login existing user
@router.post("/login", response_model=schemas.UserResponse)
def login_user(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Extract identifier and password from the request body
    identifier = request.identifier
    password = request.password

    # Search user by email and username
    user = crud.get_user_by_email(db=db, email=identifier) or crud.get_user_by_username(db=db, username=identifier)
    if not user:
        raise HTTPException(status_code=404, detail="Error: User Not Found")
    
    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Password")
    
    return user

# 3. Forgot password email send 
@router.post("/forgot-password")
async def forgot_password(request: schemas.ForgotPasswordRequest, db: Session = Depends(get_db)):
    email = request.email
    # Check if the email exists
    user = crud.get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Email not registered")
    
    # Generate a secure reset token
    reset_token = str(uuid.uuid4())
    user.reset_token = reset_token  # Store token in the database
    db.commit()

    # Generate reset link
    reset_link = f"http://yourdomain.com/reset-password?token={reset_token}"

    await send_reset_email(to_email=email, reset_link=reset_link)

    return {"message": "A password reset link has been sent to your email."}

# 4. Reset password
@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(get_db)):
    # Extract token and new password from the request
    token = request.token
    new_password = request.new_password

    # Verify token and fetch user
    user = crud.get_user_by_token(db=db, token=request.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")
    
    # Hash the new password
    hashed_password = generate_password_hash(request.new_password)
    # Update the user's password in the database
    user.hashed_password = hashed_password
    db.commit()

    return {"message": "Your password has been reset successfully."}
