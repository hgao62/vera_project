from extract_data import (
    get_stock_history,
    get_stock_financials,
    get_news,
    get_exchange_rate,
)


def main():
    """_summary_"""
    stock = "TSLA"
    print(get_stock_history(stock))
    print(get_stock_financials(stock))
    rate = get_exchange_rate(stock, "5d", "1d", "GBP")
    print(rate)
    news = get_news(stock)
    print(news)


if __name__ == "__main__":
    # test commit
    main()
