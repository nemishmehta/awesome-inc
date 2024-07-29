from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext  # type: ignore
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from typing import Annotated
from .config import TokenData


class Authentication:
    def __init__(self, stored_credentials, secret_key, algorithm):
        self.stored_credentials = stored_credentials
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.secret_key, algorithm=self.algorithm
        )
        return encoded_jwt

    def authenticate_user(self, username: str, password: str):
        if username != self.stored_credentials.username:
            return False
        if not self.verify_password(
            password, self.stored_credentials.hashed_password
        ):
            return False
        return self.stored_credentials

    def decode_token(
        self,
        token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl="token"))],
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
            username: str = payload.get("sub")
            token_data = TokenData(username=username)
        except InvalidTokenError:
            raise credentials_exception
        if token_data.username != self.stored_credentials.username:
            raise credentials_exception
        return True
