# 🧠 Portfolio Doctor – Backend (FastAPI)

A clean, scalable FastAPI backend built with **clear architectural boundaries**, **secure authentication**, and **maintainable domain-driven structure**.

---

## 📌 Tech Stack

- **FastAPI** – API framework
- **SQLAlchemy (ORM)** – Database access
- **PostgreSQL** – Relational database
- **Pydantic** – Request/response validation
- **JWT** – Authentication
- **bcrypt / Argon2** – Password hashing
- **Alembic** – Database migrations
- **Uvicorn** – ASGI server

---

## 🧱 Architecture Overview

This project follows a **layered architecture** inspired by Clean Architecture principles.

### High-level flow

Client
↓
Router (FastAPI)
↓
Service (Business Logic)
↓
Repository (DB Access)
↓
Database

### Core principles

- Routers handle **HTTP only**
- Services contain **business logic**
- Repositories talk to the **database**
- Models represent **persisted data**
- Schemas represent **API contracts**
- No FastAPI imports in services or repositories

This ensures:
- Testability
- Clear separation of concerns
- Easy refactoring
- Framework independence at the core

---

## 📂 Project Structure

app/
├── api/
│   ├── v1/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   └── portfolios.py
│   │   └── init.py
│   └── init.py
│
├── services/
│   ├── auth_service.py
│   ├── user_service.py
│   └── portfolio_service.py
│
├── repository/
│   ├── auth_repository.py
│   ├── user_repository.py
│   └── portfolio_repository.py
│
├── models/
│   ├── user.py
│   ├── portfolio.py
│   └── init.py
│
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── portfolio.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── exceptions.py
│
├── db/
│   ├── base.py
│   ├── session.py
│
├── main.py
└── init.py

---

## 📁 Folder Responsibilities

### `api/`
- FastAPI routers
- Request/response handling
- Dependency injection
- HTTPException mapping

📌 No business logic here

---

### `services/`
- Core business logic
- Authentication rules
- Session handling
- Domain validations

📌 Framework-agnostic  
📌 Raises domain exceptions, not HTTP errors

---

### `repository/`
- Database queries
- SQLAlchemy ORM usage
- Persistence logic only

📌 No business decisions  
📌 No FastAPI imports  

---

### `models/`
- SQLAlchemy ORM models
- Database schema definitions
- Relationships and constraints

📌 Represents how data is stored

---

### `schemas/`
- Pydantic models
- Request validation
- Response serialization

📌 Represents how data moves across the API

---

### `core/`
Shared infrastructure code:
- `security.py` → hashing, token logic
- `config.py` → environment & settings
- `exceptions.py` → domain-level exceptions

---

### `db/`
- `base.py` → SQLAlchemy Base
- `session.py` → DB session management

📌 Centralized DB lifecycle

---

## 🔐 Authentication Design

### Login flow

email + password
↓
AuthService.authenticate_user
↓
Password verification
↓
JWT issued

### Authorization flow

Request
↓
JWT validation (dependency)
↓
Current user injected
↓
Protected route logic

### Key rules

- Passwords are hashed before DB insert
- Passwords are never stored or logged
- Credentials are checked only once
- Sessions are validated on every request

---

### Exception Handling Strategy

| Layer | Exception Type |
|------|---------------|
Repository | SQLAlchemy / DB errors |
Service | Domain exceptions |
Router | HTTPException |

Example:

```python
# service
raise AuthenticationError()

# router
except AuthenticationError:
    raise HTTPException(status_code=401)

```
⸻

### Database Strategy
	-	SQLAlchemy ORM for CRUD
	-	PostgreSQL as primary DB
	-	Alembic for migrations
	-	DB-level constraints enforced
	-	ON DELETE CASCADE for relationships

⸻

### Running the Project

Install dependencies

pip install -r requirements.txt

Run the server

uvicorn app.main:app --reload

⸻

### Development Notes
	-	.env is never committed
	-	.venv is ignored
	-	Dev-only DB resets are guarded
	-	Logging is environment-aware

⸻

### Scalability Considerations

This architecture supports:
	-	Versioned APIs (v1, v2)
	-	External integrations
	-	Async migration later
	-	Microservice extraction
	-	Background tasks
	-	Caching layers

⸻

### Design Philosophy

Explicit is better than implicit
Simple over clever
Business logic over frameworks

This project favors clarity, safety, and long-term maintainability over shortcuts.

⸻

### Final Note

This backend is intentionally structured to:
	-	scale without rewrites
	-	onboard new developers easily
	-	survive production realities