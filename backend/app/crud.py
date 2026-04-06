from sqlalchemy.orm import Session
from . import models, schemas, auth

# User operations
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Student operations
def get_students(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Student)
    if search:
        query = query.filter(models.Student.name.ilike(f"%{search}%") | models.Student.student_id.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()

def get_student_by_user_id(db: Session, user_id: int):
    return db.query(models.Student).filter(models.Student.user_id == user_id).first()

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, db_student: models.Student, student_update: schemas.StudentUpdate):
    update_data = student_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, db_student: models.Student):
    db.delete(db_student)
    db.commit()

# Course operations
def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()

def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Grade operations
def create_grade(db: Session, grade: schemas.GradeCreate, teacher_id: int):
    db_grade = models.Grade(**grade.model_dump(), teacher_id=teacher_id)
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade

def get_student_grades(db: Session, student_id: int):
    return db.query(models.Grade).filter(models.Grade.student_id == student_id).all()
