from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Country, Customer, Installation, Product, ProductCategory
from .requests import retrieve_all_table_names, retrieve_table_data
from .core.database import get_db
from sqlalchemy.orm import Session
from .enums import ORMTables
from typing import Annotated, Union
from .core.config import (
    _ACCESS_TOKEN_EXPIRE_MINUTES,
    _SECRET_KEY,
    _ALGORITHM,
    _STORED_CREDENTIALS,
    Token,
)
from .core.authentication import Authentication

from datetime import timedelta

app = FastAPI()


def auth() -> Authentication:
    """
    Returns an instance of the `Authentication` class initialized with the
    stored credentials, secret key, and algorithm.

    :return: An instance of the `Authentication` class.
    :rtype: Authentication
    """
    return Authentication(
        stored_credentials=_STORED_CREDENTIALS,
        secret_key=_SECRET_KEY,
        algorithm=_ALGORITHM,
    )


decode_token = auth().decode_token


@app.get("/", tags=["Root"])
def root():
    """
    A function that handles the root endpoint of the API.

    Returns:
        dict: A dictionary containing a message with information about the API.
    """
    return {
        "message": "APIs to extract operational data of Awesome Inc. "
        "Check /docs for more details."
    }


@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Annotated[Authentication, Depends(auth)],
) -> Token:
    """
    Authenticates a user and generates an access token for them.

    Args:
        form_data (Annotated[OAuth2PasswordRequestForm, Depends()]): The
        form data containing the username and password.
        auth (Annotated[Authentication, Depends(auth)]): The authentication
        class used to authenticate the user.

    Returns:
        Token: A Token object containing the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect.

    """
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/all-tables")
def retrieve_table_names(
    decoded_token: Annotated[bool, Depends(decode_token)],
) -> dict:
    """
    Retrieves all table names from the database.

    This function is a GET endpoint that retrieves all table names from the
    database. It expects a valid decoded token as a dependency.

    Parameters:
        decoded_token (Annotated[bool, Depends(decode_token)]): The decoded
        token obtained from the `decode_token` dependency.

    Returns:
        dict: A dictionary containing the table names. The keys are the table
        names and the values are empty lists.
    """

    return retrieve_all_table_names()


@app.get(
    "/{table_name}",
    response_model=Union[
        list[Country],
        list[Customer],
        list[Installation],
        list[Product],
        list[ProductCategory],
    ],
)
def read_table_data(
    table_name: str,
    decoded_token: Annotated[bool, Depends(decode_token)],
    db: Session = Depends(get_db),
):
    """
    Retrieves data from a specified table in the database.

    This function is a GET endpoint that retrieves data from a specified table
    in the database. It expects a valid decoded token as a dependency. The
    table name is specified as a parameter.

    Parameters:
        table_name (str): The name of the table to retrieve data from.
        decoded_token (Annotated[bool, Depends(decode_token)]): The decoded
        token obtained from the `decode_token` dependency.
        db (Session, optional): The database session. Defaults to the result
        of the `get_db` dependency.

    Raises:
        HTTPException: If the specified table does not exist in the database.

    Returns:
        Union[list[Country], list[Customer], list[Installation], list[Product],
        list[ProductCategory]]: A list of data from the specified table.
    """

    if table_name not in retrieve_all_table_names()["table_names"]:
        raise HTTPException(
            status_code=404, detail=f"{table_name} table does not exist."
        )
    return retrieve_table_data(db, ORMTables[table_name].value)
