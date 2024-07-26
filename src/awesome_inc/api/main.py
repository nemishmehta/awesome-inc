from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import Country, Customer, Installation, Product, ProductCategory
from .requests import retrieve_all_table_names, retrieve_table_data
from .core.database import get_session
from sqlalchemy.orm import Session
from .enums import ORMTables
from typing import Annotated, Union
from .constants import ACCESS_TOKEN_EXPIRE_MINUTES
from .core.authentication import Token, Authentication

from datetime import timedelta

app = FastAPI()

# auth = Authentication()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "APIs to extract operational data of Awesome Inc. "
        "Check /docs for more details."
    }


def create_auth():
    return Authentication()


# auth = Authentication()


@app.post("/token")
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    auth: Annotated[Authentication, Depends(create_auth)],
) -> Token:
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/all-tables")
def retrieve_table_names(
    current_user: Annotated[str, Depends(create_auth().get_user)],
):
    return retrieve_all_table_names()


# TODO: Figure out an approach to generate the response_model value dynamically
# based on table_name value.
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
    current_user: Annotated[str, Depends(create_auth().get_user)],
    db: Session = Depends(get_db),
):
    if table_name not in retrieve_all_table_names()["table_names"]:
        raise HTTPException(
            status_code=404, detail=f"{table_name} table does not exist."
        )
    return retrieve_table_data(db, ORMTables[table_name].value)
