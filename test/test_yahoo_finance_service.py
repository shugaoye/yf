import pytest
from api.yahoo_finance_service import YahooFinanceService
from datetime import datetime

def test_get_stock_price_valid_start_date():
    symbol = 'EPAM'
    date = '2025-02-27'
    price, close_date = YahooFinanceService.get_stock_price(symbol, date)
    assert price is not None, "Price should not be None for a valid date"
    assert close_date == datetime.strptime('2025-03-03', '%Y-%m-%d').date(), "Close date should match the input date"

def test_get_stock_price_last_trading_date():
    symbol = 'EPAM'
    price, close_date = YahooFinanceService.get_stock_price(symbol)
    assert price is not None, "Price should not be None for a valid date"

def test_get_stock_price_invalid_date():
    symbol = 'EPAM'
    date = '1900-01-01'
    price, close_date = YahooFinanceService.get_stock_price(symbol, date)
    assert price is None, "Price should be None for an invalid date"

def test_get_stock_price_date_as_datetime():
    symbol = 'EPAM'
    date = datetime(2023, 1, 1)
    price, close_date = YahooFinanceService.get_stock_price(symbol, date)
    assert price is not None, "Price should not be None for a valid datetime object"

def test_get_stock_price_invalid_symbol():
    symbol = 'INVALID'
    date = '2023-01-01'
    price, close_date = YahooFinanceService.get_stock_price(symbol, date)
    assert price is None, "Price should be None for an invalid symbol"

def test_get_stock_prices_valid_symbols():
    symbols = ['EPAM', 'MSFT']
    start_date = '2023-01-01'
    end_date = '2023-01-10'
    prices, close_date = YahooFinanceService.get_stock_prices(symbols, start_date, end_date)
    assert all(price is not None for price in prices.values()), "Prices should not be None for valid symbols and dates"
    assert close_date == datetime.strptime('2023-01-09', '%Y-%m-%d').date(), "Close date should match the input date"

def test_get_stock_prices_last_trading_date():
    symbols = ['EPAM', 'MSFT']
    prices, close_date = YahooFinanceService.get_stock_prices(symbols)
    print(prices)
    assert all(price is not None for price in prices.values()), "Prices should not be None for valid symbols"

def test_get_stock_prices_invalid_dates():
    symbols = ['EPAM', 'MSFT']
    start_date = '1900-01-01'
    end_date = '1900-01-10'
    prices, close_date = YahooFinanceService.get_stock_prices(symbols, start_date, end_date)
    assert all(price is None for price in prices.values()), "Prices should be None for invalid dates"

def test_get_stock_prices_date_as_datetime():
    symbols = ['EPAM', 'MSFT']
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 10)
    prices, close_date = YahooFinanceService.get_stock_prices(symbols, start_date, end_date)
    assert all(price is not None for price in prices.values()), "Prices should not be None for valid datetime objects"

def test_get_stock_prices_invalid_symbols():
    symbols = ['INVALID1', 'INVALID2']
    start_date = '2023-01-01'
    end_date = '2023-01-10'
    prices, close_date = YahooFinanceService.get_stock_prices(symbols, start_date, end_date)
    assert all(price is None for price in prices.values()), "Prices should be None for invalid symbols"




