import bcrypt

# Hash a plain-text password
def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt=salt).decode("utf-8")

# Verify password against its hash
def verify_password(plain_password: str, hashed_password: str) -> str:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))