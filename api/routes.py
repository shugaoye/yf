# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
from flask import request, jsonify
from flask_restx import Api, Resource, fields

from api.models import db, Datas, YData
from api.yahoo_finance_service import YahooFinanceService

rest_api = Api(version="1.1", title="Yahoo Finance Data API")

"""
API Interface:
   
   - /datas
       - GET: return all items
       - POST: create a new item
   
   - /datas/:id
       - GET    : get item
       - PUT    : update item
       - DELETE : delete item
"""

"""
Flask-RestX models Request & Response DATA
"""

SECRET_KEY = os.environ.get("SECRET_KEY")

# Used to validate input data for creation
create_model = rest_api.model('CreateModel', {"data": fields.String(required=True, min_length=1, max_length=255)})

# Used to validate input data for update
update_model = rest_api.model('UpdateModel', {"data": fields.String(required=True, min_length=1, max_length=255)})

# Used to validate input data for YahooFinanceData creation
create_yahoo_model = rest_api.model('CreateYahooModel', {
    "symbol": fields.String(required=True, min_length=1, max_length=10),
    "price": fields.Float(required=True),
    "date": fields.DateTime(required=False)
})

# Used to validate input data for YahooFinanceData update
update_yahoo_model = rest_api.model('UpdateYahooModel', {
    "symbol": fields.String(required=False, min_length=1, max_length=10),
    "price": fields.Float(required=False),
    "date": fields.DateTime(required=False)
})

# Define a new model to validate the input data for fetching stock prices
symbols_model = rest_api.model('SymbolsModel', {
    "symbols": fields.List(fields.String(required=True, min_length=1, max_length=10), required=True),
    "start_date": fields.String(required=False),
    "end_date": fields.String(required=False)
})

def verify_signature(request):
    # Extract the signature from the Authorization header
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("HMAC "):
        return False, "Invalid signature format"

    expected_signature = auth_header.split(" ")[1]

    # Create the canonical message to hash
    method = request.method
    url = request.url
    headers = request.headers.copy()
    # Exclude the Authorization header itself from the message
    del headers["Authorization"]
    # Include a timestamp to prevent replay attacks
    if "X-Timestamp" not in headers:
        return False, "Missing X-Timestamp header"
    body = request.get_data(as_text=True)

    # Construct the message
    message = f"{method}\n{url}\n{headers}\n{body}"

    # Generate the expected signature
    try:
        computed_signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    except Exception as e:
        return False, f"Signature verification failed: {str(e)}"

    return computed_signature == expected_signature, None

# Custom decorator to enforce HMAC authentication
def require_hmac(f):
    def decorated(*args, **kwargs):
        valid, error = verify_signature(request)
        if not valid:
            return error, 401
        return f(*args, **kwargs)
    return decorated

"""
    Flask-Restx routes
"""

@rest_api.route('/api/datas')
class Items(Resource):

    """
       Return all items
    """
    @require_hmac
    def get(self):

        items = Datas.query.all()
        
        return {"success" : True,
                "msg"     : "Items found ("+ str(len( items ))+")",
                "datas"   : str( items ) }, 200

@rest_api.route('/api/stock_prices')
class StockPrices(Resource):

    """
       Fetch stock prices for a list of symbols
    """
    @rest_api.expect(symbols_model, validate=True)
    def post(self):

        # Read ALL input  
        req_data = request.get_json()

        # Get the information    
        symbols = req_data.get("symbols")
        start_date = req_data.get("start_date")
        end_date = req_data.get("end_date")

        # Fetch stock prices
        prices, close_date = YahooFinanceService.get_stock_prices(symbols, start_date, end_date)
        
        # Format close_date to a string in "YYYY-MM-DD" format
        if close_date:
            close_date = close_date.strftime('%Y-%m-%d')

        return {"success": True,
                "msg": "Stock prices fetched successfully",
                "close_date": close_date,
                "data": prices}, 200
