'''test functions for the project'''
import pytest
import pandas as pd
from extract_data import get_stock_history, get_news


class TestStockData:
    """Test cases for stock data related functions"""
    @pytest.fixture
    def sample_stock_history(self):
        """Fixture to provide sample stock history data"""
        return get_stock_history(self)

    @pytest.fixture
    def sample_stock_news(self):
        """Fixture to provide sample stock news data"""
        return get_news(self)

    def test_get_stock_history_returns_dataframe(self, sample_stock_history):
        """Test if get_stock_history returns a DataFrame"""
        assert isinstance(sample_stock_history, pd.DataFrame)

    def test_get_stock_history_columns(self, sample_stock_history):
        """Test if get_stock_history returns DataFrame with expected columns"""
        expected_columns = ['date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'stock']
        assert sample_stock_history.columns.tolist() == expected_columns

    def test_get_news_returns_dataframe(self, sample_stock_news):
        """Test if get_news returns a DataFrame"""
        assert isinstance(sample_stock_news, pd.DataFrame)

    def test_get_news_columns(self, sample_stock_news):
        """Test if get_news returns DataFrame with expected columns"""
        expected_columns = ['stock',
                            'uuid',
                            'title',
                            'publisher',
                            'link',
                            'providerPublishTime',
                            'type']
        assert sample_stock_news.columns.tolist() == expected_columns
