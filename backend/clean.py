import os
from dotenv import load_dotenv
load_dotenv()
from app.database import SessionLocal
from app.models import User, Student, Course, Grade

def clean():
    db = SessionLocal()
    print("Deleting grades...")
    db.query(Grade).delete()
    print("Deleting students...")
    db.query(Student).delete()
    print("Deleting courses...")
    db.query(Course).delete()
    print("Deleting users...")
    db.query(User).delete()
    db.commit()
    print("Cleaned database")
    db.close()

if __name__ == "__main__":
    clean()
