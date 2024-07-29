from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext  # type: ignore
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, HTTPException, status
from typing import Annotated
from .config import TokenData
from awesome_inc.api.core.config import Credentials


class Authentication:
    """
    A class that provides methods for authentication and token management.

    Attributes:
        stored_credentials: A dictionary containing the username and hashed
        password of the stored credentials.
        secret_key: A secret key used for encoding and decoding tokens.
        algorithm: The algorithm used for encoding and decoding tokens.
    """

    def __init__(
        self, stored_credentials: Credentials, secret_key: str, algorithm: str
    ):
        self.stored_credentials = stored_credentials
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        """
        Verify if the given plain password matches the hashed password.

        Args:
            plain_password (str): The plain password to be verified.
            hashed_password (str): The hashed password to be compared with the
            plain password.

        Returns:
            bool: True if the plain password matches the hashed password,
            False otherwise.
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        """
        Generate a hashed password using the provided password.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password.
        """
        return self.pwd_context.hash(password)

    def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        """
        Generate an access token for the given data.

        Args:
            data (dict): The data to be encoded in the access token.
            expires_delta (timedelta, optional): The duration for which the
            access token should be valid. Defaults to None.

        Returns:
            str: The encoded access token.
        """

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
        """
        Authenticates a user by checking if the username and hashed password match.

        Args:
            username (str): The username of the user to authenticate.
            password (str): The password of the user to authenticate.

        Returns:
            dict: The stored credentials if the username and hashed password
            match, False otherwise.
        """
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
        """
        Decodes a JWT token and validates the credentials.

        Args:
            token (Annotated[str,
            Depends(OAuth2PasswordBearer(tokenUrl="token"))]): The JWT token to
            be decoded.

        Returns:
            bool: True if the token is successfully decoded and the credentials
            are valid.

        Raises:
            HTTPException: If the token cannot be validated or if the username
            in the token does not match the stored credentials.
        """

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
