from fastapi.testclient import TestClient
from awesome_inc.api.main import app, get_db, decode_token, auth
from awesome_inc.api.core.config import (
    Credentials,
)
from unittest.mock import MagicMock
from datetime import timedelta
from sqlalchemy.orm import Session


client = TestClient(app)


# Mock the Authentication class
class MockAuth:
    def authenticate_user(self, username: str, password: str):
        if username == "valid_user" and password == "valid_password":
            return MagicMock(
                Credentials, username=username, hashed_password=password
            )
        else:
            return False

    def create_access_token(self, data: dict, expires_delta: timedelta):
        return "mock_access_token"

    def decode_token(self, token: str = "Bearer valid_token"):
        if token == "Bearer valid_token":
            return True
        else:
            return False


def mock_auth():
    return MockAuth()


app.dependency_overrides[auth] = mock_auth
app.dependency_overrides[decode_token] = MockAuth().decode_token


def override_get_db():
    yield MagicMock(spec=Session)


app.dependency_overrides[get_db] = override_get_db


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "APIs to extract operational data of Awesome Inc."
        " Check /docs for more details."
    }


def test_login_success():
    response = client.post(
        "/token", data={"username": "valid_user", "password": "valid_password"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "mock_access_token",
        "token_type": "bearer",
    }


def test_login_failure():
    response = client.post(
        "/token",
        data={"username": "invalid_user", "password": "invalid_password"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_retrieve_all_tables(mocker):
    mock_retrieve_all_table_names = mocker.patch(
        "awesome_inc.api.main.retrieve_all_table_names"
    )
    mock_retrieve_all_table_names.return_value = {
        "table_names": ["country", "customer"]
    }

    response = client.get(
        "/all-tables", headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 200
    assert response.json() == {"table_names": ["country", "customer"]}


def test_read_table_data_valid(mocker):
    mock_retrieve_all_table_names = mocker.patch(
        "awesome_inc.api.main.retrieve_all_table_names"
    )
    mock_retrieve_all_table_names.return_value = {
        "table_names": ["country", "customer"]
    }
    mock_retrieve_table_data = mocker.patch(
        "awesome_inc.api.main.retrieve_table_data"
    )
    mock_retrieve_table_data.return_value = [{"id": 1, "name": "Country1"}]

    response = client.get(
        "/country", headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Country1"}]


def test_read_table_data_invalid(mocker):
    mock_retrieve_all_table_names = mocker.patch(
        "awesome_inc.api.main.retrieve_all_table_names"
    )
    mock_retrieve_all_table_names.return_value = {
        "table_names": ["country", "customer"]
    }

    response = client.get(
        "/InvalidTable", headers={"Authorization": "Bearer valid_token"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "InvalidTable table does not exist."}
