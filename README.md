# Task Manager API

A **FastAPI**-based **Task Manager API** with **JWT authentication**, supporting:

- **Access & refresh tokens**  
- **Token rotation** (refresh token rotation for security)  
- **Secure user authentication**  
- **Task management**:
  - Create, read, update, and delete tasks
  - Tasks are linked to specific users
  - Protected routes for authenticated users only

---

## Features

- **User Registration & Login**
  - Passwords hashed using **bcrypt**
  - JWT **access tokens** (short-lived)  
  - JWT **refresh tokens** (long-lived, rotated on use)

- **Token-based Authentication**
  - Protected routes using `OAuth2PasswordBearer`
  - Access token validation
  - Refresh token rotation and revocation

- **Tasks Management**
  - Create, update, delete, and list tasks
  - Tasks are linked to specific users

- **Secure Refresh Tokens**
  - Refresh tokens stored **hashed** in DB
  - Rotation ensures old tokens are invalidated
  - Expiration checks for tokens

- **Error Handling**
  - Custom exceptions for invalid credentials, missing users, tasks, or tokens
  - 401 Unauthorized for expired or revoked tokens

---

## Tech Stack

- **Backend Framework:** FastAPI  
- **Database:** SQLAlchemy + SQLite 
- **Authentication:** JWT  
- **Password Hashing:** Passlib (bcrypt)  
- **Dependency Management:** Python `venv` + `requirements.txt`  

---

