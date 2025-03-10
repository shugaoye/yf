import pytest
from api.yahoo_finance_service import YahooFinanceService
from datetime import datetime

def test_get_stock_price_valid_start_date():
    symbol = 'EPAM'
    date = '2025-02-27'
    price = YahooFinanceService.get_stock_price(symbol, date)
    assert price is not None, "Price should not be None for a valid date"

def test_get_stock_price_last_trading_date():
    symbol = 'EPAM'
    price = YahooFinanceService.get_stock_price(symbol)
    assert price is not None, "Price should not be None for a valid date"

def test_get_stock_price_invalid_date():
    symbol = 'EPAM'
    date = '1900-01-01'
    price = YahooFinanceService.get_stock_price(symbol, date)
    assert price is None, "Price should be None for an invalid date"

def test_get_stock_price_date_as_datetime():
    symbol = 'EPAM'
    date = datetime(2023, 1, 1)
    price = YahooFinanceService.get_stock_price(symbol, date)
    assert price is not None, "Price should not be None for a valid datetime object"

def test_get_stock_price_invalid_symbol():
    symbol = 'INVALID'
    date = '2023-01-01'
    price = YahooFinanceService.get_stock_price(symbol, date)
    assert price is None, "Price should be None for an invalid symbol"



