"""_summary_
"""
from enum import Enum
import pandas as pd
import yfinance as yf

class StockData(Enum):
    """_summary_

    Args:
        Enum (_type_): _description_
    """    
    DATE = 'date'
    STOCKSPLITS = 'Stock Splits'
    DIVIDENDS = 'Dividends'
    STOCK = 'stock'

def get_stock_history(stock:str):
    """_summary_
    Args:
        stock (str): _description_
    Returns:
        pd.DataFrame: _description_
    """
    ticker = yf.Ticker(stock)
    result = ticker.history(period="6d")
    result.reset_index(inplace = True)
    result.drop(columns = [StockData.STOCKSPLITS.value], inplace = True)
    result[StockData.DIVIDENDS.value] = result[StockData.DIVIDENDS.value].astype(int)
    result.columns = result.columns.str.lower()
    result[StockData.STOCK.value] = stock
    result[StockData.DATE.value] = result[StockData.DATE.value].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return result

def get_stock_financials(stock:str):
    """_summary_
    Args:
        stock (str): _description_
    Returns:
        pd.DataFrame: _description_
    """
    ticker = yf.Ticker(stock)
    shares = ticker.income_stmt
    shares = shares.iloc[:17].T
    shares.reset_index(inplace = True)
    shares = shares.rename(columns = {'index' : StockData.DATE.value})
    shares[StockData.DATE.value] = shares[StockData.DATE.value].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return shares
