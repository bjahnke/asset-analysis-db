import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from asset_db.client import MyStock
from sqlalchemy.engine import URL
from sqlalchemy.sql import text

connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="password",
    host='localhost',
    port=5432,
    database="asset_analysis"
)

Session = sessionmaker(bind=create_engine(connection_url))

def clear_tables(session):
    session.execute(text("DELETE FROM stock_data"))
    session.execute(text("DELETE FROM stock"))
    session.commit()

@pytest.fixture(scope='module')
def test_session():
    engine = create_engine(connection_url)
    Session = sessionmaker(bind=engine)
    return Session

def test_get_or_create(test_session):

    stock = MyStock(
        symbol="AAPL",
        is_relative=False,
        interval="1d",
        data_source="api_example",
        market_index="NASDAQ",
        sec_type="stock"
    )
    with test_session() as session:
        clear_tables(session)
        retrieved_stock = stock.get_or_create(session)
        assert retrieved_stock.id is not None

        # Test retrieving the same stock again
        same_stock = stock.get_or_create(session)
        assert same_stock.id == retrieved_stock.id

def test_add_stock_data(test_session):
    stock = MyStock(
        symbol="AAPL",
        is_relative=False,
        interval="1d",
        data_source="api_example",
        market_index="NASDAQ",
        sec_type="stock"
    )
    data = pd.DataFrame({
        'timestamp': pd.date_range(start='2022-01-01', periods=5, freq='D').astype(str),  # Convert to string format
        'open': [150, 152, 153, 155, 157],
        'high': [155, 156, 158, 160, 162],
        'low': [149, 151, 152, 154, 156],
        'close': [154, 155, 157, 159, 161],
        'volume': [1000, 1100, 1200, 1300, 1400]
    })
    with test_session() as session:
        clear_tables(session)
        stock_id = stock.add_stock_data(data, session)
        assert stock_id is not None

        # Verify data was inserted
        result = session.execute(
            text("SELECT COUNT(*) FROM stock_data WHERE stock_id = :stock_id"), 
            {'stock_id': stock_id}
        ).scalar()
        assert result == 5

        stock.add_stock_data(data, session)

        # Verify that data with the same id and timestamp was not inserted
        assert result == 5
