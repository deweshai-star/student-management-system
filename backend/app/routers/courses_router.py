from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, auth, database, models

router = APIRouter(
    prefix="/courses",
    tags=["Courses"],
)

@router.post("/", response_model=schemas.CourseResponse, dependencies=[Depends(auth.require_role([models.RoleEnum.admin]))])
def create_course(course: schemas.CourseCreate, db: Session = Depends(database.get_db)):
    return crud.create_course(db=db, course=course)

@router.get("/", response_model=List[schemas.CourseResponse])
def read_courses(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.get_courses(db, skip=skip, limit=limit)

@router.post("/grades", response_model=schemas.GradeResponse, dependencies=[Depends(auth.require_role([models.RoleEnum.teacher]))])
def assign_grade(grade: schemas.GradeCreate, db: Session = Depends(database.get_db), current_teacher: models.User = Depends(auth.get_current_user)):
    student = crud.get_student(db, student_id=grade.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    course = db.query(models.Course).filter(models.Course.id == grade.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.create_grade(db=db, grade=grade, teacher_id=current_teacher.id)

@router.get("/students/{student_id}/grades", response_model=List[schemas.GradeResponse])
def get_student_grades_endpoint(student_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role == models.RoleEnum.student:
        student = crud.get_student_by_user_id(db, user_id=current_user.id)
        if not student or student.id != student_id:
            raise HTTPException(status_code=403, detail="Not authorized to view these grades")
    return crud.get_student_grades(db=db, student_id=student_id)
