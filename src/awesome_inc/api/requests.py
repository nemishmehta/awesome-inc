from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from .core.database import new_engine


def retrieve_all_table_names():
    metadata = MetaData()
    metadata.reflect(bind=new_engine())
    return {"table_names": list(metadata.tables)}


def retrieve_table_data(db: Session, model):
    return db.query(model).all()
