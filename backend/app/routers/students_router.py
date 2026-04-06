from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, auth, database, models

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)

@router.post("/", response_model=schemas.StudentResponse, dependencies=[Depends(auth.require_role([models.RoleEnum.admin]))])
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == student.user_id).first()
    if not db_user or db_user.role != models.RoleEnum.student:
        raise HTTPException(status_code=400, detail="Invalid user ID or user is not a student")
    db_student = crud.get_student_by_user_id(db, user_id=student.user_id)
    if db_student:
        raise HTTPException(status_code=400, detail="Student profile already exists for this user")
    return crud.create_student(db=db, student=student)

@router.get("/", response_model=List[schemas.StudentResponse], dependencies=[Depends(auth.require_role([models.RoleEnum.admin, models.RoleEnum.teacher]))])
def read_students(skip: int = 0, limit: int = 100, search: str = None, db: Session = Depends(database.get_db)):
    return crud.get_students(db, skip=skip, limit=limit, search=search)

@router.get("/me", response_model=schemas.StudentResponse)
def read_student_me(current_user: models.User = Depends(auth.require_role([models.RoleEnum.student])), db: Session = Depends(database.get_db)):
    student = crud.get_student_by_user_id(db, user_id=current_user.id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student

@router.get("/{student_id}", response_model=schemas.StudentResponse, dependencies=[Depends(auth.require_role([models.RoleEnum.admin, models.RoleEnum.teacher]))])
def read_student(student_id: int, db: Session = Depends(database.get_db)):
    student = crud.get_student(db, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{student_id}", response_model=schemas.StudentResponse, dependencies=[Depends(auth.require_role([models.RoleEnum.admin]))])
def update_student(student_id: int, student_update: schemas.StudentUpdate, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return crud.update_student(db=db, db_student=db_student, student_update=student_update)

@router.delete("/{student_id}", response_model=dict, dependencies=[Depends(auth.require_role([models.RoleEnum.admin]))])
def delete_student(student_id: int, db: Session = Depends(database.get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    crud.delete_student(db=db, db_student=db_student)
    return {"detail": "Student deleted"}
