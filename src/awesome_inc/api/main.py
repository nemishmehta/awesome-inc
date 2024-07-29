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
    return Authentication(
        stored_credentials=_STORED_CREDENTIALS,
        secret_key=_SECRET_KEY,
        algorithm=_ALGORITHM,
    )


decode_token = auth().decode_token


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "APIs to extract operational data of Awesome Inc. "
        "Check /docs for more details."
    }


@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Annotated[Authentication, Depends(auth)],
) -> Token:
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
):
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
    if table_name not in retrieve_all_table_names()["table_names"]:
        raise HTTPException(
            status_code=404, detail=f"{table_name} table does not exist."
        )
    return retrieve_table_data(db, ORMTables[table_name].value)
