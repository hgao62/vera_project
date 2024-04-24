"""Extract stock data using yahoo finance api"""
from enum import Enum
import pandas as pd
import yfinance as yf

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

class StockData(Enum):
    """Enum for stock related attributes"""
    DATE = 'Date'
    STOCKSPLITS = 'Stock Splits'
    DIVIDENDS = 'Dividends'
    STOCK = 'stock'
    EXCHANGEID = 'exchange_id'
    CURRENCYDATEKEY = 'currency_date_key'
    TOCURRENCY = 'ToCurrency'
    FROMCURRENCY = 'FromCurrency'
    TICKER = 'Ticker'
    CURRENCYCODE = 'currency_code'
    OPEN = 'Open'
    ADJCLOSE = 'Adj Close'
    LOW = 'Low'
    HIGH = 'High'
    CURRENCYCLOSE = 'currency_close'


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
    result[StockData.DATE.value] = result[StockData.DATE.value].apply(lambda x: x.strftime(DATE_FORMAT))
    result[StockData.DIVIDENDS.value] = result[StockData.DIVIDENDS.value].astype(int)
    result.columns = result.columns.str.lower()
    result[StockData.STOCK.value] = stock
    
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

def get_exchange_rate(stock, period, interval, to_currency):
    """This function downloads exchange rate changes of a certain currency from yahoo finance api
    Args:
        stock (str): stock name you want to download the income statement for 
    """
    ticker = yf.Ticker(stock)
    currency_code = ticker.fast_info['currency']
    fx_rate_ticker = f'{currency_code}{to_currency}=X'
    fx_rate = yf.download(fx_rate_ticker, period=period, interval=interval)
    fx_rate.reset_index(inplace = True)
    currency_date_key = fx_rate[StockData.DATE.value].apply(lambda x: x.strftime('%m%d%Y'))
    exchange_id = currency_date_key + currency_code
    fx_rate[StockData.DATE.value] = fx_rate[StockData.DATE.value].apply(lambda x: x.strftime(DATE_FORMAT))
    fx_rate[StockData.EXCHANGEID.value] = exchange_id
    fx_rate[StockData.CURRENCYDATEKEY.value] = currency_date_key
    fx_rate[StockData.TOCURRENCY.value] = to_currency
    fx_rate[StockData.FROMCURRENCY.value] = currency_code
    fx_rate[StockData.TICKER.value] = stock
    fx_rate[StockData.CURRENCYCODE.value] = currency_code
    fx_rate = fx_rate.loc[:, [StockData.TICKER.value,
                              StockData.CURRENCYCODE.value,
                              StockData.DATE.value,
                              StockData.OPEN.value,
                              StockData.ADJCLOSE.value,
                              StockData.LOW.value,
                              StockData.HIGH.value,
                              StockData.FROMCURRENCY.value,
                              StockData.TOCURRENCY.value,
                              StockData.EXCHANGEID.value,
                              StockData.CURRENCYDATEKEY.value]]
    fx_rate = fx_rate.rename(columns = {StockData.ADJCLOSE.value : StockData.CURRENCYCLOSE.value})
    return fx_rate


def get_news(stock):
    """This function downloads stock news information from yahoo finance api
    Args:
        stock (str): stock name that is used to download the related news
    """
    ticker = yf.Ticker(stock)
    news = ticker.news
    df = pd.DataFrame(news)
    df[StockData.STOCK.value] = stock
    df = df.loc[:, [StockData.STOCK.value, 'uuid', 'title', 'publisher', 'link', 'providerPublishTime', 'type']]
    return df