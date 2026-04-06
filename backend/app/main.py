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

app.include_router(auth_router.router)
app.include_router(students_router.router)
app.include_router(courses_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Student Management System API"}
