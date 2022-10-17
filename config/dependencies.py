import os

from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$ySdA7vA7DGjFf/eZket4R.bdoh7P8qI7SuHCscnyKFgGOzydm8pyi",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "6580b6eced1861b5ad3a6fab3fdaf92267cd3929283124c0c2cd90215358d9de",
        "disabled": True,
    },
}

SECRET_KEY = "afef793d11c787da31d394f5eaeadd0e682012edabd2f5a61e00d47b4c224d8e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Settings(BaseSettings):
    db_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


load_dotenv()

settings = Settings(
    # db_url=os.environ['DB_URL'],
    db_url="postgresql://postgres:123@127.0.0.1:5432/stock_trades_db",
    secret_key=os.environ['SECRET_KEY'],
    algorithm=os.environ['ALGORITHM'],
    access_token_expire_minutes=os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'],
)


api_router = APIRouter()
