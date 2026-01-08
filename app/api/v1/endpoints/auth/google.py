from fastapi import APIRouter, Request, Depends, HTTPException, status
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session

from app.api.v1.dependency import get_auth_service
from app.db.session import get_db
from app.schemas.auth import RegisterResponse
from app.core.config import settings

google_router = APIRouter()
oauth = OAuth()
auth_service = get_auth_service()

google = oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid profile email"},
)


@google_router.get("/login/google")
async def login_with_google(request: Request):
    """
    Docstring for login_with_google

    :param request: Description
    :type request: Request
    """

    redirect_uri = request.url_for("google_callback")
    if google:
        return await google.authorize_redirect(request, redirect_uri)


@google_router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Docstring for google_callback

    :param request: Description
    :type request: Request
    """
    if google:
        token = await google.authorize_access_token(request)
        user = token.get("userinfo")
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Google login failed!"
            )
        new_user = auth_service.register_user_by_identity(
            db, email=user["email"], google_id=user["sub"]
        )
        return RegisterResponse(
            user_id=new_user.id,
            email=new_user.email,
            is_active=new_user.is_active,
            created_at=new_user.created_at,
        )
