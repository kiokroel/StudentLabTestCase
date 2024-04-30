from pathlib import Path

from dotenv import load_dotenv
import os

from pydantic import BaseModel
from pydantic.v1 import BaseSettings

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")


BASE_DIR = Path(__file__).parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
