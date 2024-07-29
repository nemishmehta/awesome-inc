from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from awesome_inc.api.requests import (
    retrieve_all_table_names,
    retrieve_table_data,
)
from sqlalchemy.engine import Engine
from awesome_inc.api.models import Country


def test_retrieve_all_table_names(mocker):
    mock_engine = mocker.patch("awesome_inc.api.requests.new_engine")
    mock_engine.return_value = MagicMock(spec=Engine)

    mock_metadata = MagicMock()
    mock_metadata.tables = {"table1": None, "table2": None}

    mock_metadata_class = mocker.patch("awesome_inc.api.requests.MetaData")
    mock_metadata_class.return_value = mock_metadata

    result = retrieve_all_table_names()

    assert result == {"table_names": ["table1", "table2"]}


def test_retrieve_table_data(mocker):
    mock_db = mocker.patch("awesome_inc.api.core.database.get_db")
    mock_db.return_value = MagicMock(spec=Session)

    mock_model = Country(
        id=1,
        name="Country1",
        region="Region1",
    )
    mock_query = mock_db.query.return_value
    mock_query.all.return_value = [mock_model]

    result = retrieve_table_data(mock_db, Country)

    assert result == [mock_model]
