from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from typing import Optional, List
from .models import RoleEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: RoleEnum

class UserResponse(UserBase):
    id: int
    role: RoleEnum
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[RoleEnum] = None

class StudentBase(BaseModel):
    name: str
    student_id: str
    grade: str
    enrollment_date: date
    profile_picture_url: Optional[str] = None

class StudentCreate(StudentBase):
    user_id: int

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    grade: Optional[str] = None
    profile_picture_url: Optional[str] = None

class StudentResponse(StudentBase):
    id: int
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    credits: int

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class GradeBase(BaseModel):
    student_id: int
    course_id: int
    grade_value: str

class GradeCreate(GradeBase):
    pass

class GradeResponse(GradeBase):
    id: int
    teacher_id: int
    model_config = ConfigDict(from_attributes=True)
