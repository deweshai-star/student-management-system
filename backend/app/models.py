from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum

class RoleEnum(enum.Enum):
    admin = "admin"
    teacher = "teacher"
    student = "student"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

    student_profile = relationship("Student", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String, index=True, nullable=False)
    student_id = Column(String, unique=True, index=True, nullable=False)
    grade = Column(String, nullable=False)
    enrollment_date = Column(Date, nullable=False)
    profile_picture_url = Column(String, nullable=True)

    user = relationship("User", back_populates="student_profile")
    grades = relationship("Grade", back_populates="student")

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    credits = Column(Integer, nullable=False)

    grades = relationship("Grade", back_populates="course")

class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    grade_value = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
    teacher = relationship("User")
