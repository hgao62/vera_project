from extract_data import get_stock_history, get_stock_financials

def main():
    """_summary_
    """
    stock = 'MSFT'
    print(get_stock_history(stock))
    print(get_stock_financials(stock))

if __name__ == "__main__":
    main()