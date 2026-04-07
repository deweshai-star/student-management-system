# Student Management System

A production-ready Student Management System built with React (Vite), Tailwind CSS, shadcn/ui, Python FastAPI, and PostgreSQL.

## Features
- **Authentication**: JWT-based role-based access control (Admin, Teacher, Student)
- **Student Profile**: Complete CRUD for students.
- **Course Management**: Admins create courses, Teachers assign grades.
- **Beautiful UI**: Modern, responsive dashboard using Tailwind and shadcn/ui.

## Quick Start (Without Docker / Windows PowerShell)

Because the Neon Cloud Database is already seeded and active, you can launch the app locally using a single PowerShell command!

1. Open PowerShell in the root directory of this project.
2. Run the following command to instantly start both the Backend API and the React Frontend in their own windows:
   ```powershell
   Start-Process powershell -ArgumentList "-NoExit -Command `"cd backend; python -m uvicorn app.main:app --port 8000`""; Start-Process powershell -ArgumentList "-NoExit -Command `"cd frontend; npm run dev`""
   ```
3. Once the windows pop up and finish loading, navigate to **http://localhost:5173** in your browser to view the application!

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
