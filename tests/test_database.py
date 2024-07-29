from awesome_inc.api.core.database import get_db
from sqlalchemy.orm import Session


def test_get_db():
    db = next(get_db())
    assert isinstance(db, Session)
