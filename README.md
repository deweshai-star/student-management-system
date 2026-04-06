# Student Management System

A production-ready Student Management System built with React (Vite), Tailwind CSS, shadcn/ui, Python FastAPI, and PostgreSQL.

## Features
- **Authentication**: JWT-based role-based access control (Admin, Teacher, Student)
- **Student Profile**: Complete CRUD for students.
- **Course Management**: Admins create courses, Teachers assign grades.
- **Beautiful UI**: Modern, responsive dashboard using Tailwind and shadcn/ui.

## Quick Start (Docker)

1. Make sure you have Docker and Docker Compose installed.
2. Run the following command in the root directory:
   ```bash
   docker-compose up --build
   ```
3. The database will be seeded automatically (Admin, Teacher, Students).

## Access Points
- **Frontend App**: [http://localhost:5173](http://localhost:5173)
- **Backend API & Swagger Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Demo Accounts

Password for all accounts is: `password123`

- Admin: `admin@example.com`
- Teacher: `teacher@example.com`
- Student 1: `student1@example.com`
- Student 2: `student2@example.com`

Enjoy!
