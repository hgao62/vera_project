"""Extract stock data using yahoo finance api"""
from enum import Enum
import pandas as pd
import yfinance as yf

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class StockData(Enum):
    """Enum for stock related attributes"""
    DATE = 'date'
    STOCKSPLITS = 'Stock Splits'
    DIVIDENDS = 'Dividends'
    STOCK = 'stock'

def get_stock_history(stock:str):
    """This function donwloads historical stockprices from yahoo finance api
    Args:
        stock (str): stock name you want to download price for
    Returns:
        pd.DataFrame: records price marks of the stock for 6 days 
    """
    ticker = yf.Ticker(stock)
    result = ticker.history(period="6d")
    result.reset_index(inplace = True)
    result.drop(columns = [StockData.STOCKSPLITS.value], inplace = True)
    result[StockData.DIVIDENDS.value] = result[StockData.DIVIDENDS.value].astype(int)
    result.columns = result.columns.str.lower()
    result[StockData.STOCK.value] = stock
    result[StockData.DATE.value] = result[StockData.DATE.value].apply(lambda x: x.strftime(DATE_FORMAT))
    return result

def get_stock_financials(stock:str):
    """This function downloads stock financials(income statement) from yahoo finance api
    Args:
        stock (str): stock name you want to download the income statement for 
    Returns:
        pd.DataFrame: the stock income statement information of recent four years
    """
    ticker = yf.Ticker(stock)
    shares = ticker.income_stmt
    shares = shares.T
    shares.reset_index(inplace = True)
    shares = shares.rename(columns = {'index' : StockData.DATE.value})
    shares[StockData.DATE.value] = shares[StockData.DATE.value].apply(lambda x: x.strftime(DATE_FORMAT))
    return shares
