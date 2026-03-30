Task Manager REST API Demo
Quick Start (Local)

Activate virtual environment
\venv\Scripts\Activate    

Run the application:

python run.py

Open interactive API docs:

http://127.0.0.1:8000/docs
🔐 Authentication (Important)

This API uses JWT (JSON Web Tokens) to protect task-related endpoints.
You must authenticate before accessing any CRUD operations for tasks.

How to Test the API (Full Flow)
1️⃣ Register a user

Endpoint:

POST /auth/register

Example:

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "123456"
}
2️⃣ Login

Endpoint:

POST /auth/login

Response:

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR...",
  "token_type": "bearer"
}
3️⃣ Authorize (🔓 Button in Swagger UI)

In /docs:

Click Authorize (top right)
Enter the token in this format:
Bearer YOUR_TOKEN_HERE

Example:

Bearer eyJhbGciOiJIUzI1NiIsInR...
Click Authorize → Close
4️⃣ Use Task Endpoints

Now you can access:

POST /tasks -> Create task
GET /tasks -> Get your tasks
PUT /tasks/{id} -> Update task
DELETE /tasks/{id} -> Delete task
Without Authentication

If you don’t authorize, you will get:

{
  "detail": "Not authenticated"
}

What This Project Demonstrates
Secure authentication with JWT
Password hashing (bcrypt)
Full REST API (CRUD)
User-based access control
PostgreSQL integration (production-ready)
Live Demo

You can test the deployed API here:

https://task-manager-api-j538.onrender.com/docs
