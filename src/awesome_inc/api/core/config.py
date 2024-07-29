from pydantic import BaseModel
import os


class Credentials(BaseModel):
    username: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


_STORED_CREDENTIALS: Credentials = Credentials(
    username=os.environ["ADF__USERNAME"],
    hashed_password=os.environ["HASHED__PASSWORD"],
)

_SECRET_KEY: str = os.environ["SECRET__KEY"]
_ALGORITHM: str = "HS256"
_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
