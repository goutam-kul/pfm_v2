from fastapi import FastAPI
from db.database import engine
from app.models import Base
from app.routes import users, expense, budgets
from utils.scheduler import start_scheduler

# Create the FastAPI app instance
app = FastAPI(title="Personal Finance Manager v2")

# Create the database tables if not already exists
Base.metadata.create_all(bind=engine)

# Include the centralized router
# Include individual routers directly
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(expense.router, prefix="/expenses", tags=["expenses"])
app.include_router(budgets.router, prefix="/budgets", tags=["budgets"])

# Root endpoint for health check or welcome message
@app.get("/")
def read_root():
    return {"message": "Yo Koso! Watshi no Soul Society Ae"}

if __name__ == "__main__":
    import uvicorn
    start_scheduler()
    uvicorn.run(app=app, host="0.0.0.0", port=6000)