from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from db.database import SessionLocal
from app.models import Budget
from datetime import datetime

def reset_monthly_budgets():
    """
    Resets the current_total for all budgets at the start of each month.
    """
    db: Session = SessionLocal()
    try:
        # Reset current_total for all budgets
        db.query(Budget).update({Budget.current_total: 0.0})  # Explicitly set the column to 0.0
        db.commit()
        print("Monthly budget totals have been reset.")
    except Exception as e:
        print(f"Error resetting monthly budgets: {e}")
    finally:
        db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(reset_monthly_budgets, "cron", day=1, hour=0)
    scheduler.start()
    print("Scheduler started and reset job added.")

# if __name__ == "__main__":
#     reset_monthly_budgets()