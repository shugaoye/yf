import yfinance as yf
from datetime import datetime, timedelta

def process_dates(start_date=None, end_date=None):
    # Check if start_date is a string and convert to datetime
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    
    # Check if end_date is a string and convert to datetime
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    
    # If start_date is provided but end_date is not, set end_date to start_date + 5 days
    if start_date and not end_date:
        end_date = start_date + timedelta(days=5)
    
    # If start_date is not provided, set end_date to today and start_date to end_date - 5 days
    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=5)
    
    return start_date, end_date

class YahooFinanceService:
    @staticmethod
    def get_stock_price(symbol, start_date=None, end_date=None):
        """
        Fetches the stock price for a given symbol between the specified start and end dates.
        If no dates are provided, it fetches the price for the last trading date.

        Args:
            symbol (str): The stock symbol to fetch data for.
            start_date (str or datetime, optional): The start date for fetching data. Defaults to None.
            end_date (str or datetime, optional): The end date for fetching data. Defaults to None.

        Returns:
            float or None: The closing stock price on the last available date within the specified range, or None if no data is available.
        """
        start_date, end_date = process_dates(start_date, end_date)
        delta = end_date - start_date

        print(f"Fetching stock data for {symbol} from {start_date} to {end_date}, total days: {delta.days}")
        
        # Fetch stock data
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date)
        print(hist)

        # Check if data is available for the given date
        if not hist.empty:
            return hist['Close'].iloc[-1]
        else:
            return None
