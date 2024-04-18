import sys
import pandas as pd
import yfinance as yf


stock = sys.argv[1]
ticker = yf.Ticker(stock)

def get_stock_history(stock:str) -> pd.DataFrame:
    """_summary_
    Args:
        stock (str): _description_
    Returns:
        pd.DataFrame: _description_
    """
    result = ticker.history(period="6d")
    result.reset_index(inplace = True)
    result.drop(columns = ['Stock Splits'], inplace = True)
    result['Dividends'] = result['Dividends'].astype(int)
    result.columns = result.columns.str.lower()
    result['stock'] = stock
    result['date'] = result['date'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return result


history = get_stock_history(stock)
print(history)

def get_stock_financials(stock:str) -> pd.DataFrame:
    """_summary_
    Args:
        stock (str): _description_
    Returns:
        pd.DataFrame: _description_
    """
    shares = ticker.income_stmt
    shares = shares.iloc[:17].T
    shares.reset_index(inplace = True)
    shares = shares.rename(columns = {'index' : 'date'})
    shares['date'] = shares['date'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S.%f'))
    return shares

finance = get_stock_financials(stock)
print(finance)


