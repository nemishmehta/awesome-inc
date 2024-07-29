from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
from sqlalchemy.engine.url import URL
from pydantic import BaseModel
import os
import logging

logger = logging.getLogger(__name__)


class Database(BaseModel):
    hostname: str
    username: str
    password: str
    dbname: str
    port: int

    def sqlalchemy_url(self) -> URL:
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.username,
            password=self.password,
            host=self.hostname,
            port=self.port,
            database=self.dbname,
        )


def new_engine() -> Engine:
    try:
        database = Database(
            hostname=os.environ["DATABASE__HOSTNAME"],
            username=os.environ["DATABASE__USERNAME"],
            password=os.environ["DATABASE__PASSWORD"],
            dbname=os.environ["DATABASE__DB"],
            port=int(os.environ["DATABASE__PORT"]),
        )
    except KeyError:
        logger.error(
            "Database credentials not found. Were environment variables"
            " correctly set?"
        )
    uri = database.sqlalchemy_url()
    return create_engine(uri, echo=True)


def get_session() -> Session:
    sessionlocal = sessionmaker(
        bind=new_engine(), autocommit=False, autoflush=False
    )
    return sessionlocal()


def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
