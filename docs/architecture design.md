# 🏗 Architecture Design Document

## Overview

This project follows a **layered architecture** with clear separation of concerns.  
The goal is to build a backend that is:

- Maintainable
- Testable
- Framework-agnostic at its core
- Safe to evolve as requirements grow

The architecture intentionally avoids mixing **transport concerns (FastAPI)** with **business logic**, and avoids overusing **dependency injection** where it provides no lifecycle benefit.

---

## Architectural Layers

API Layer (FastAPI Routers)
↓
Service Layer (Business Logic)
↓
Repository Layer (Persistence)
↓
Database

Each layer has **strict responsibilities** and **one-directional dependencies**.

---

## 1️⃣ API Layer (FastAPI Routers)

### Responsibilities

- Handle HTTP requests and responses
- Parse and validate input (via Pydantic schemas)
- Inject dependencies (DB session, current user)
- Convert domain errors into HTTP errors

### What belongs here

- `@router.get/post/...`
- `Depends(...)`
- `HTTPException`
- Status codes
- Request / response models

### What does NOT belong here

- Business rules
- Database queries
- Password hashing
- External API orchestration

### Why this separation matters

FastAPI is a **transport framework**, not a business framework.

Keeping HTTP concerns at the edge ensures:
- Business logic can be reused outside HTTP
- Tests don’t require a running FastAPI app
- The core logic survives framework changes

---

## 2️⃣ Service Layer (Business Logic)

### Responsibilities

- Core business rules
- Authentication logic
- Authorization decisions
- Session handling
- Orchestration of repositories and external APIs

### What belongs here

- Domain logic
- Validation beyond schema-level checks
- Password hashing and verification
- Domain-specific exceptions

### What does NOT belong here

- `HTTPException`
- FastAPI imports
- Status codes
- Request / response objects

---

## ❌ Why NOT use `HTTPException` in services

### Problem

Using `HTTPException` in services couples business logic to FastAPI.

```python
# ❌ Wrong
raise HTTPException(status_code=401)

Consequences
	•	Service becomes unusable outside FastAPI
	•	Business logic is no longer framework-agnostic
	•	Testing requires HTTP semantics
	•	Architecture becomes brittle

✅ Correct approach

Services raise domain exceptions:

class AuthenticationError(Exception):
    pass

Routers translate them:

except AuthenticationError:
    raise HTTPException(status_code=401)

Principle

Services speak business. Routers speak HTTP.

⸻

3️⃣ Repository Layer (Persistence)

Responsibilities
	•	Database access
	•	ORM queries
	•	Mapping persisted data to domain objects

What belongs here
	•	SQLAlchemy queries
	•	select, insert, db.add
	•	Simple CRUD operations

What does NOT belong here
	•	Business decisions
	•	Authentication rules
	•	HTTP or FastAPI imports
	•	Domain-level exceptions

Why repositories stay “dumb”

Repositories should answer how, not why.

They fetch and persist data, nothing more.

⸻

4️⃣ Why Depends Should Be Avoided for Services

Common misconception

“Everything should be injected using Depends”

This is not true.

⸻

What Depends is actually for

FastAPI dependency injection is designed to manage:
	•	Lifecycle (create → use → cleanup)
	•	Request-scoped objects
	•	Context-aware dependencies

Examples:
	•	DB sessions
	•	Current user
	•	OAuth tokens
	•	Request headers

⸻

Why services don’t need Depends

Most services are:
	•	Stateless
	•	Lightweight
	•	Pure business logic
	•	Safe to reuse

Injecting them via Depends adds:
	•	Unnecessary indirection
	•	Framework coupling
	•	Harder debugging
	•	Harder testing (dependency overrides)

⸻

❌ Overuse of Depends

def get_auth_service():
    return AuthService(AuthRepository())

@router.post("/login")
def login(auth_service: AuthService = Depends(get_auth_service)):
    ...

This manages nothing useful.

⸻

✅ Preferred approach

Use module-level singletons for stateless services:

auth_service = AuthService(AuthRepository())

This is:
	•	Explicit
	•	Simple
	•	Predictable
	•	Easy to test

⸻

When Depends is appropriate for services

Use DI only if the service:
	•	Needs request-scoped data
	•	Requires setup/teardown
	•	Depends on current user or request context
	•	Manages async resources

Otherwise, avoid it.

⸻

5️⃣ Exception Handling Strategy

Layer-wise exception responsibilities

Layer	Exception Type
API	HTTPException
Service	Domain exceptions
Repository	DB / ORM exceptions

Flow

Repository error
   ↓
Service translates to domain error
   ↓
Router translates to HTTP error

Benefits
	•	Clear responsibility boundaries
	•	Centralized HTTP behavior
	•	Reusable business logic
	•	Cleaner tests

⸻

6️⃣ Session & Authentication Design

Credentials vs Sessions
	•	Credentials are verified once (login)
	•	Sessions are validated per request

Where sessions live
	•	JWTs
	•	Database
	•	Redis

Where sessions do NOT live
	•	In-memory service attributes
	•	Global variables

Services remain stateless and query session storage when needed.

⸻

7️⃣ Database & ORM Strategy
	•	SQLAlchemy ORM for application logic
	•	db.add() for standard CRUD
	•	Core insert() / select() only when justified
	•	DB-level constraints enforced
	•	Cascades defined at DB level, not only ORM

⸻

8️⃣ Testing Implications

This architecture enables:
	•	Unit tests for services without FastAPI
	•	Repository tests with a test DB
	•	Router tests focused only on HTTP behavior
	•	No mocking of FastAPI internals for business tests

⸻

9️⃣ Design Principles
	•	Explicit over implicit
	•	Stateless services
	•	Thin routers
	•	Dumb repositories
	•	Business logic independent of frameworks
	•	Avoid overengineering early

⸻

Summary

Key decisions
	•	FastAPI is restricted to the API layer
	•	Services never raise HTTP exceptions
	•	Dependency Injection is used sparingly
	•	Business logic is framework-agnostic
	•	Architecture favors long-term maintainability

⸻

Final Thought

Frameworks change. Business rules should not.

This architecture ensures the system can evolve without painful rewrites.

---

If you want next, I can:
- add **Mermaid diagrams**
- convert this into a **formal ADR**
- tailor it for **code reviewers**
- simplify it for **college submission**
- map rules → linting checks

Just tell me where this document is going.