# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os

from flask import Flask
from flask_cors import CORS

from api.routes import rest_api
from api.models import db

# Create App
app = Flask(__name__)

# load Config 
app.config.from_object('api.config.BaseConfig')

# Connect Flask and SqlAlchemy
db.init_app(app)

# Connect Flask and FlaskRestX
rest_api.init_app(app)

# Enable CORS
CORS(app)

# Setup database
@app.before_request
def initialize_database():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True