from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from fastapi_backend.config.dependencies import settings, oauth2_scheme, fake_users_db, api_router
from fastapi_backend.src.storage.schemas.users import User, Token
from fastapi_backend.src.usecase.users.utils import get_current_active_user, authenticate_user, create_access_token

router = APIRouter(
    # prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": f"username:{user.username}"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
