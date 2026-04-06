import os
import time
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models, auth
from app.schemas import UserCreate
from app.crud import create_user
from datetime import date

def wait_for_db():
    print("Waiting for database...")
    retries = 10
    while retries > 0:
        try:
            # this will throw if db is not ready
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            print("Database is ready!")
            return
        except Exception as e:
            retries -= 1
            print(f"Database not ready, retrying in 2 seconds... ({retries} left)")
            time.sleep(2)
    print("Could not connect to the database.")

def seed_db():
    # Only seed if no users exist
    db = SessionLocal()
    
    users_count = db.query(models.User).count()
    if users_count > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    print("Seeding database...")
    
    # 1. Create Admin
    admin_user = create_user(db, UserCreate(email="admin@example.com", password="password123", role=models.RoleEnum.admin))
    
    # 2. Create Teacher
    teacher_user = create_user(db, UserCreate(email="teacher@example.com", password="password123", role=models.RoleEnum.teacher))
    
    # 3. Create Students
    student1_user = create_user(db, UserCreate(email="student1@example.com", password="password123", role=models.RoleEnum.student))
    student2_user = create_user(db, UserCreate(email="student2@example.com", password="password123", role=models.RoleEnum.student))
    
    student1 = models.Student(user_id=student1_user.id, name="Alice Smith", student_id="STU001", grade="10th", enrollment_date=date(2023, 9, 1))
    student2 = models.Student(user_id=student2_user.id, name="Bob Jones", student_id="STU002", grade="11th", enrollment_date=date(2022, 9, 1))
    
    db.add(student1)
    db.add(student2)
    
    # 4. Create Courses
    math_course = models.Course(title="Math 101", description="Introduction to Mathematics", credits=3)
    science_course = models.Course(title="Science 101", description="Introduction to Science", credits=4)
    
    db.add(math_course)
    db.add(science_course)
    
    db.commit()
    
    print("Database seeded successfully done!")
    db.close()

if __name__ == "__main__":
    wait_for_db()
    
    # Ensure tables are created
    models.Base.metadata.create_all(bind=engine)
    
    seed_db()
