from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import (
    TokenResponse,
    LoginRequest,
    RegisterRequest,
    RegisterResponse,
)
from app.db.session import get_db
from sqlalchemy.orm import Session
from app.api.v1.dependency import get_auth_service
from app.exception.exceptions import UserAlreadyExists

local_router = APIRouter()
auth_service = get_auth_service()


@local_router.post("/login", response_model=TokenResponse)
def login_user(user: LoginRequest, db: Session = Depends(get_db)):
    try:
        db_user = auth_service.authenticate_user(db, user.email, user.password)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password or user doesn't exist",
            )
        return {"access_token": "", "token_type": ""}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)


@local_router.post("/register", response_model=RegisterResponse)
def register_user(user: RegisterRequest, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.register_user(db, user.email, user.password)
        return RegisterResponse(
            user_id=new_user.id,
            email=new_user.email,
            is_active=new_user.is_active,
            created_at=new_user.created_at,
        )
    except UserAlreadyExists as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e)
