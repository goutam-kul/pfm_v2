from db.database import engine
from app.models import Base

def init_db():
    print("Intializing the database...")
    Base.metadata.create_all(bind=engine)
    print("Database Initialized.")

if __name__ == "__main__":
    init_db()