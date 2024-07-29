import pytest
from datetime import timedelta
from awesome_inc.api.core.authentication import Authentication
from awesome_inc.api.core.config import Credentials
from fastapi import HTTPException, status
import jwt


@pytest.fixture
def auth():
    # Set up the environment variables for testing
    ADF__USERNAME = "testuser@awesomeinc.com"
    HASHED__PASSWORD = "$2b$12$aCW83wGC2lueQTF9F3gwt.d7zrKkU4feJnR3/qrPFMOwwE7kvw6da"  # bcrypt hash for "password"
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"

    _stored_credentials = Credentials(
        username=ADF__USERNAME,
        hashed_password=HASHED__PASSWORD,
    )

    return Authentication(
        stored_credentials=_stored_credentials,
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
    )


def test_verify_password(auth):
    assert auth.verify_password(
        "password", auth.stored_credentials.hashed_password
    )


def test_verify_incorrect_password(auth):
    assert not auth.verify_password(
        "wrongpassword", auth.stored_credentials.hashed_password
    )


def test_get_password_hash(auth):
    password = "newpassword"
    hashed_password = auth.get_password_hash(password)
    assert auth.verify_password(password, hashed_password)


def test_create_access_token(auth):
    data = {"sub": "testuser@awesomeinc.com"}
    token = auth.create_access_token(data)
    decoded_data = jwt.decode(
        token,
        auth.secret_key,
        algorithms=[auth.algorithm],
    )
    assert decoded_data["sub"] == "testuser@awesomeinc.com"


def test_create_access_token_with_expiry(auth):
    data = {"sub": "testuser@awesomeinc.com"}
    token_with_expiry = auth.create_access_token(
        data, expires_delta=timedelta(minutes=5)
    )
    decoded_data_with_expiry = jwt.decode(
        token_with_expiry,
        auth.secret_key,
        algorithms=[auth.algorithm],
    )
    assert decoded_data_with_expiry["sub"] == "testuser@awesomeinc.com"


def test_check_exp_in_token(auth):
    data = {"sub": "testuser@awesomeinc.com"}
    token_with_expiry = auth.create_access_token(
        data, expires_delta=timedelta(minutes=5)
    )
    decoded_data_with_expiry = jwt.decode(
        token_with_expiry,
        auth.secret_key,
        algorithms=[auth.algorithm],
    )
    assert "exp" in decoded_data_with_expiry


def test_authenticate_user(auth):
    assert auth.authenticate_user("testuser@awesomeinc.com", "password")


def test_authenticate_incorrect_password(auth):
    assert not auth.authenticate_user(
        "testuser@awesomeinc.com", "wrongpassword"
    )


def test_authenticate_incorrect_username(auth):
    assert not auth.authenticate_user("wronguser", "password")


def test_decode_token(auth):
    data = {"sub": "testuser@awesomeinc.com"}
    token = auth.create_access_token(data)

    # Mock the dependency injection in FastAPI
    def fake_oauth2_password_bearer():
        return token

    assert auth.decode_token(fake_oauth2_password_bearer())


def test_decode_invalid_token(auth):
    with pytest.raises(HTTPException) as excinfo:
        invalid_token = "invalidtoken"
        auth.decode_token(invalid_token)
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
