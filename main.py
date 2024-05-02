from extract_data import get_stock_history, get_stock_financials, get_news, get_exchange_rate, enrich_stock_history
from typing import List
from load_data import save_df_to_db
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)s  - %(message)s", level=logging.INFO, filename='project_logging.log')
logger = logging.getLogger(__name__)

def main(stocks: List[str], period: str, interval:str, db_type:str):
    """_summary_
    """

    # print(get_stock_history(stock))
    # print(get_stock_financials(stock))
    # rate = get_exchange_rate(stock, '5d', '1d', 'GBP')
    # print(rate)
    # news = get_news(stock)
    # print(news)
    # enrich = enrich_stock_history(get_stock_history(stock))
    # print(enrich)
    for stock in stocks:
        stock_history = get_stock_history(stock)
        stock_financials = get_stock_financials(stock)
        rate = get_exchange_rate(stock, period, interval, 'GBP')
        news = get_news(stock)


        save_df_to_db(stock_history, 'stock_history')
        save_df_to_db(stock_financials, 'stock_financials')
        save_df_to_db(rate, 'exchange_rate')
        save_df_to_db(news, 'news')

if __name__ == "__main__":
    stocks = [
        "TSLA",
        "AAPL",
        "GOOGL",
        "AMZN",
        "MSFT",
        "TSM",
        "NVDA",
        "JPM",
        "JNJ",
    ]
    logger.info('Process started.')
    main(stocks, '5d', '1d', 'mysql')
    logger.info('Process finished.')