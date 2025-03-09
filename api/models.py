# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import datetime
import pytz

import json

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Datas(db.Model):

    id           = db.Column(db.Integer()   , primary_key=True)
    data         = db.Column(db.String(256) , nullable=False)
    date_created = db.Column(db.DateTime()  , default=lambda: datetime.now(pytz.utc))

    def __repr__(self):
        return str( self.id ) 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_data(self, new_data):
        self.data = new_data

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def toDICT(self):

        cls_dict         = {}
        cls_dict['_id']  = self.id
        cls_dict['data'] = self.data

        return cls_dict

    def toJSON(self):

        return self.toDICT()

class YData(db.Model):

    id     = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), nullable=False)
    price  = db.Column(db.Float, nullable=False)
    date   = db.Column(db.DateTime, default=lambda: datetime.now(pytz.utc))

    def __repr__(self):
        return f"<YahooFinanceData {self.symbol}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_data(self, symbol=None, price=None, date=None):
        if symbol:
            self.symbol = symbol
        if price:
            self.price = price
        if date:
            self.date = date

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def toDICT(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'price': self.price,
            'date': self.date
        }

    def toJSON(self):
        return self.toDICT()

