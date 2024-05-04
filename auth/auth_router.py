from database import get_db
from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from auth import utils as auth_utils
from app.schemas import UserCreate, User
from sqlalchemy.ext.asyncio import AsyncSession

from app.services import users as crud

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(prefix="/auth", tags=["Авторизация"])


async def validate_auth_user(username: str = Form(), password: str = Form(), db: AsyncSession = Depends(get_db)
                             ) -> User | Exception:
    email = username
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    if not (user := await crud.get_user_by_email(db, email=email)):
        raise unauthed_exc

    if not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc

    return user


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}")
    return payload


async def get_current_auth_user(payload: dict = Depends(get_current_token_payload),
                                db: AsyncSession = Depends(get_db)) -> User:
    email: str | None = payload.get("sub")
    if user := await crud.get_user_by_email(db, email):
        return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid (user not found)")


@router.post("/login/", response_model=TokenInfo)
def auth_user_issue_jwt(user: UserCreate = Depends(validate_auth_user)):
    jwt_payload = {
        "sub": user.email,
        "username": user.username,
        "email": user.email
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/users/me/")
def auth_user_check_self_info(payload: dict = Depends(get_current_token_payload),
                              user: User = Depends(get_current_auth_user)):
    iat = payload.get("iat")
    return {"username": user.username, "email": user.email, "logged_in_at": iat, "id": user.id}
