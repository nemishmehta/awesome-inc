from sqlalchemy.orm import Session
from sqlalchemy import MetaData
from .core.database import new_engine


def retrieve_all_table_names():
    """
    Retrieves all table names from the database.

    Returns:
        dict: A dictionary containing the table names as keys and an empty list
        as values.
    """

    metadata = MetaData()
    metadata.reflect(bind=new_engine())
    return {"table_names": list(metadata.tables)}


def retrieve_table_data(db: Session, model):
    """
    Retrieves all data from the specified table in the database.

    Args:
        db (Session): The database session object.
        model (Model): The model representing the table to retrieve data
        from.

    Returns:
        List[Model]: A list of all the rows in the specified table.
    """
    return db.query(model).all()
