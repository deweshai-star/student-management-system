from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError
from . import models, database
from .routers import auth_router, students_router, courses_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Student Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(OperationalError)
async def db_not_connected_handler(request: Request, exc: OperationalError):
    return JSONResponse(
        status_code=503,
        content={"message": "Database is not connected. Please ensure the database server is running and the connection string is correct."},
    )

app.include_router(auth_router.router, prefix="/api")
app.include_router(students_router.router, prefix="/api")
app.include_router(courses_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Management System API"}

@app.get("/api/seed")
def seed_database(db: database.SessionLocal = Depends(database.get_db)):
    users_count = db.query(models.User).count()
    if users_count > 0:
        return {"message": "Database already seeded. Skipping."}
    
    from datetime import date
    from .schemas import UserCreate
    from .crud import create_user

    admin_user = create_user(db, UserCreate(email="admin@example.com", password="password123", role=models.RoleEnum.admin))
    teacher_user = create_user(db, UserCreate(email="teacher@example.com", password="password123", role=models.RoleEnum.teacher))
    student1_user = create_user(db, UserCreate(email="student1@example.com", password="password123", role=models.RoleEnum.student))
    student2_user = create_user(db, UserCreate(email="student2@example.com", password="password123", role=models.RoleEnum.student))
    
    student1 = models.Student(user_id=student1_user.id, name="Alice Smith", student_id="STU001", grade="10th", enrollment_date=date(2023, 9, 1))
    student2 = models.Student(user_id=student2_user.id, name="Bob Jones", student_id="STU002", grade="11th", enrollment_date=date(2022, 9, 1))
    db.add(student1)
    db.add(student2)
    
    math_course = models.Course(title="Math 101", description="Introduction to Mathematics", credits=3)
    science_course = models.Course(title="Science 101", description="Introduction to Science", credits=4)
    db.add(math_course)
    db.add(science_course)
    db.commit()
    
    return {"message": "Database seeded successfully via API!"}
