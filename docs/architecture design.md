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
# 🏗 Architecture Design Document

## Overview

This project follows a **layered architecture** with clear separation of concerns.
The goal is to build a backend that is:

- Maintainable
- Testable
- Framework-agnostic at its core
- Safe to evolve as requirements grow

The architecture intentionally avoids mixing **transport concerns (FastAPI)** with **business logic**, and avoids overusing dependency injection where it provides no lifecycle benefit.

---

## Architectural Layers

1. API Layer (FastAPI routers)
2. Service Layer (Business logic)
3. Repository Layer (Persistence)
4. Database

Each layer has strict responsibilities and one-directional dependencies.

---

## 1. API Layer (FastAPI Routers)

### Responsibilities

- Handle HTTP requests and responses
- Parse and validate input (via Pydantic schemas)
- Inject request-scoped dependencies (DB session, current user)
- Convert domain errors into HTTP errors

### What belongs here

- `@router.get/post/...`
- `Depends(...)` (for request-scoped objects)
- `HTTPException`
- Status codes
- Request / response models

### What does NOT belong here

- Business rules
- Database queries
- Password hashing
- External API orchestration

Keeping HTTP concerns at the edge ensures business logic can be reused outside HTTP and tests don’t require a running FastAPI app.

---

## 2. Service Layer (Business Logic)

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

Services should remain framework-agnostic so they can be reused and unit-tested without FastAPI.

---

## 3. Why NOT use `HTTPException` in services

Using `HTTPException` in services couples business logic to FastAPI.

```python
# ❌ Wrong
raise HTTPException(status_code=401)
```

Consequences:

- Service becomes unusable outside FastAPI
- Business logic is no longer framework-agnostic
- Tests require HTTP semantics
- Architecture becomes brittle

Correct approach: services raise domain exceptions and routers translate them.

```python
class AuthenticationError(Exception):
    pass

# In router
try:
    service.authenticate(...)
except AuthenticationError:
    raise HTTPException(status_code=401)
```

Principle: services speak business; routers speak HTTP.

---

## 4. Repository Layer (Persistence)

### Responsibilities

- Database access
- ORM queries
- Mapping persisted data to domain objects

### What belongs here

- SQLAlchemy queries
- `select`, `insert`, `db.add`
- Simple CRUD operations

### What does NOT belong here

- Business decisions
- Authentication rules
- HTTP or FastAPI imports
- Domain-level exceptions

Repositories should answer "how" (data access), not "why" (business rules).

---

## 5. Why `Depends` Should Be Used Carefully

FastAPI dependency injection manages lifecycle, request-scoped objects, and setup/teardown for context-aware resources. Typical examples:

- DB sessions
- Current user
- OAuth tokens
- Request headers

Most services, however, are:

- Stateless
- Lightweight
- Pure business logic
- Safe to reuse

Injecting such services via `Depends` adds unnecessary indirection and framework coupling. Prefer module-level singletons for stateless services:

```python
auth_service = AuthService(AuthRepository())
```

Use `Depends` when a service:

- Needs request-scoped data
- Requires setup/teardown
- Depends on current user or request context
- Manages async resources

---

## 6. Exception Handling Strategy

| Layer | Exception Type |
|---|---|
| API | `HTTPException` |
| Service | Domain exceptions |
| Repository | DB / ORM exceptions |

Flow:

Repository error → Service translates to domain error → Router translates to HTTP error

Benefits:

- Clear responsibility boundaries
- Centralized HTTP behavior
- Reusable business logic
- Cleaner tests

---

## 7. Session & Authentication Design

- Credentials are verified once (login)
- Sessions are validated per request

Where sessions live:

- JWTs
- Database
- Redis

Where sessions should NOT live:

- In-memory service attributes
- Global variables

Services should remain stateless and query session storage when needed.

---

## 8. Database & ORM Strategy

- Use SQLAlchemy ORM for application logic
- Use `db.add()` for standard CRUD
- Use core `insert()` / `select()` only when justified
- Enforce DB-level constraints
- Define cascades at DB level, not only in ORM

---

## 9. Testing Implications

This architecture enables:

- Unit tests for services without FastAPI
- Repository tests with a test DB
- Router tests focused only on HTTP behavior
- No mocking of FastAPI internals for business tests

---

## Design Principles

- Explicit over implicit
- Stateless services
- Thin routers
- Dumb repositories
- Business logic independent of frameworks
- Avoid over-engineering early

---

## Summary

Key decisions:

- FastAPI is restricted to the API layer
- Services never raise HTTP exceptions
- Dependency injection is used sparingly
- Business logic is framework-agnostic
- Architecture favors long-term maintainability

---

## Final Thought

Frameworks change. Business rules should not. This architecture helps the system evolve without painful rewrites.
