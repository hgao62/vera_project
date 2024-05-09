"""Extract stock data using yahoo finance api"""
from enum import Enum
import logging
import pandas as pd
import yfinance as yf


DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
logger = logging.getLogger(__name__)

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
    DAILYRETURN = 'daily_return'
    CUMRETURN = 'cummulative_return'


def get_stock_history(stock:str):
    """This function donwloads historical stockprices from yahoo finance api
    Args:
        stock (str): stock name you want to download price for
    Returns:
        pd.DataFrame: records price marks of the stock for 6 days
    """
    logger.info('Getting stock history for %s.', stock)
    ticker = yf.Ticker(stock)
    result = ticker.history(period="6d")
    result.reset_index(inplace = True)
    result.drop(columns = [StockData.STOCKSPLITS.value], inplace = True)
    result[StockData.DATE.value] = result[StockData.DATE.value].apply(
        lambda x: x.strftime(DATE_FORMAT)
        )
    result[StockData.DIVIDENDS.value] = result[StockData.DIVIDENDS.value].astype(int)
    result.columns = result.columns.str.lower()
    result[StockData.STOCK.value] = stock
    logger.info('Finished getting stock history for %s.', stock)
    return result

def get_stock_financials(stock:str):
    """This function downloads stock financials(income statement) from yahoo finance api
    Args:
        stock (str): stock name you want to download the income statement for
    Returns:
        pd.DataFrame: the stock income statement information of recent four years
    """
    logger.info('Getting stock financials for %s.', stock)
    ticker = yf.Ticker(stock)
    shares = ticker.income_stmt
    shares = shares.T
    shares.reset_index(inplace = True)
    shares = shares.rename(columns = {'index' : StockData.DATE.value})
    shares[StockData.DATE.value] = shares[StockData.DATE.value].apply(
        lambda x: x.strftime(DATE_FORMAT)
        )
    columns = [
        "date",
        "Tax Effect Of Unusual Items",
        "Tax Rate For Calcs",
        "Normalized EBITDA",
        "Net Income From Continuing Operation Net Minority Interest",
        "Reconciled Depreciation",
        "Reconciled Cost Of Revenue",
        "EBITDA",
        "EBIT",
        "Net Interest Income",
        "Interest Expense",
        "Interest Income",
        "Normalized Income",
        "Net Income From Continuing And Discontinued Operation",
        "Total Expenses",
        "Total Operating Income As Reported",
        "Diluted Average Shares",
        "Basic Average Shares",
        "Diluted EPS",
        "Basic EPS",
        "Diluted NI Availto Com Stockholders",
        "Net Income Common Stockholders",
        "Net Income",
        "Net Income Including Noncontrolling Interests",
        "Net Income Continuous Operations",
        "Tax Provision",
        "Pretax Income",
        "Other Income Expense",
        "Other Non Operating Income Expenses",
        "Net Non Operating Interest Income Expense",
        "Interest Expense Non Operating",
        "Interest Income Non Operating",
        "Operating Income",
        "Operating Expense",
        "Research And Development",
        "Selling General And Administration",
        "Gross Profit",
        "Cost Of Revenue",
        "Total Revenue",
        "Operating Revenue",
        "stock",
        ]
    common_columns = shares.columns.intersection(columns)
    shares = shares[common_columns]
    logger.info('Finished getting stock financials for %s.', stock)
    return shares

def get_exchange_rate(stock, period, interval, to_currency):
    """This function downloads exchange rate changes of a certain currency from yahoo finance api
    Args:
        stock (str): stock name you want to download the income statement for
    Returns:
        pd.DataFrame: the stock currency rate information for a given time period
    """
    logger.info('Getting stock exchange rate for %s.', stock)
    ticker = yf.Ticker(stock)
    currency_code = ticker.fast_info['currency']
    fx_rate_ticker = f'{currency_code}{to_currency}=X'
    fx_rate = yf.download(fx_rate_ticker, period=period, interval=interval)
    fx_rate.reset_index(inplace = True)
    currency_date_key = fx_rate[StockData.DATE.value].apply(
        lambda x: x.strftime('%m%d%Y')
        )
    exchange_id = currency_date_key + currency_code
    fx_rate[StockData.DATE.value] = fx_rate[StockData.DATE.value].apply(
        lambda x: x.strftime(DATE_FORMAT)
        )
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
    logger.info('Finished getting stock exchange rate for %s.', stock)
    return fx_rate

def get_news(stock):
    """This function downloads stock news information from yahoo finance api
    Args:
        stock (str): stock name that is used to download the related news
    Returns:
        pd.DataFrame: the stock news information of recent four years
    """
    logger.info('Getting stock news for %s.', stock)
    ticker = yf.Ticker(stock)
    news = ticker.news
    data = pd.DataFrame(news)
    data[StockData.STOCK.value] = stock
    data = data.loc[:, [StockData.STOCK.value,
                    'uuid',
                    'title',
                    'publisher',
                    'link',
                    'providerPublishTime',
                    'type']]
    logger.info('Finished getting stock news for %s.', stock)
    return data

def enrich_stock_history(stock_history:pd.DataFrame):
    """This function adds two columns to stock_history data frame
        a. "daily_return": this is caluclated using the "close" price column,
            google "how to calculate daily return pandas"
        b. "cummulative_return": this is caculated using the "daily_return" calculated
            from step above

    Args:
        stock_history (pd.DataFrame):
            dataframe that describes the stock history with daily return and
            cummulative return added

    Returns:
        pd.DataFrame: the stock history with daily return and cummulative return data
    """
    logger.info('Enriching stock history.')
    stock_history[StockData.DAILYRETURN.value] = stock_history.close.pct_change(1)
    stock_history[StockData.CUMRETURN.value] = (1 + stock_history.daily_return).cumprod() - 1
    logger.info('Finished enriching stock history.')
    return stock_history
