from __future__ import (absolute_import, division, print_function, unicode_literals)

from collections import namedtuple
from functools import lru_cache

import numpy as np
import pandas as pd
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from rqalpha.data.yield_curve_store import YieldCurveStore
from rqalpha.interface import AbstractDataSource
from rqalpha.model.instrument import Instrument
from rqalpha.utils.datetime_func import convert_date_to_int

from ialgotest.utils.exception import DataFeedError

INSTRUMENT_TYPE_MAP = {
    'CS': 0,
    'INDX': 1,
    'Future': 2,
    'ETF': 3,
    'LOF': 3,
    'FenjiA': 3,
    'FenjiB': 3,
    'FenjiMu': 3,
}

INSTRUMENT_COL = 'code'
TRADING_DATES_REF_CODE = '600000.SH'
FIELDS = {
    'datetime': np.uint64,
    'open': np.dtype('float64'),
    'close': np.dtype('float64'),
    'high': np.dtype('float64'),
    'low': np.dtype('float64'),
    'volume': np.uint64,
    'total_turnover': np.uint64,
}

Rule = namedtuple('Rule', ['multiplier', 'round'])
CONVERTER = {
    'open': Rule(1, 4),
    'close': Rule(1, 4),
    'high': Rule(1, 4),
    'low': Rule(1, 4),
    'limit_up': Rule(1, 4),
    'limit_down': Rule(1, 4),
}


def get_col_name(code):
    index, market = code.split('.')
    return market + '_' + index


class CycType(object):
    CYC_MINUTE = 1
    CYC_DAY = 2
    CYC_WEEK = 3
    CYC_MONTH = 4
    CYC_SEASON = 5
    CYC_HAFLYEAR = 6
    CYC_YEAR = 7
    CYC_Type_list = [CYC_MINUTE, CYC_DAY, CYC_WEEK, CYC_MONTH, CYC_SEASON, CYC_HAFLYEAR, CYC_YEAR]


class MongoDataSource(AbstractDataSource):
    def __init__(self, host='127.0.0.1', port=27017, database='emquant'):
        self.client = MongoClient(host, port)
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
        except ConnectionFailure as err:
            print('Failed to establish connection to MongoDB: %s' % err)
        self.db = self.client[database]
        self._instruments = self.get_instruments_from_mongo()
        self._trading_dates = self.get_trading_dates_from_mongo(TRADING_DATES_REF_CODE)
        self._yield_curve = YieldCurveStore('/root/.rqalpha/bundle/yield_curve.bcolz')

    def get_all_instruments(self):
        return self._instruments

    def get_trading_calendar(self):
        return self._trading_dates

    def available_data_range(self, frequency):
        if frequency == '1d':
            calendar = self.get_trading_calendar()
            return calendar[0].to_pydatetime(), calendar[-1].to_pydatetime()

        raise NotImplementedError

    def get_bar(self, instrument, dt, frequency):
        """
        :type instrument: rqalpha.model.instrument.instrument
        :type dt: datetime.datetime
        :param str frequency: `1d` or `1m`
        :return: numpy.ndarray
        """
        if frequency != '1d':
            raise NotImplementedError

        return self.get_stock_data_from_mongo(instrument.order_book_id, CycType.CYC_DAY, dt)

    def history_bars(self, instrument, bar_count, frequency, fields, dt, skip_suspended=True):
        """
        :type instrument: rqalpha.model.instrument.instrument
        :type bar_count: int
        :param str frequency: `1d` or `1m`
        :type fields: str
        :type dt: datetime.datetime
        :return: numpy.ndarray
        """
        if frequency != '1d':
            raise NotImplementedError

        bars = self.get_stock_data_hist_from_mongo(instrument.order_book_id, CycType.CYC_DAY, dt, bar_count)

        if bars is None or not self._are_fields_valid(fields, bars.dtype.names):
            return None

        if skip_suspended and instrument.type == 'CS':
            bars = bars[bars['volume'] > 0]

        if fields is None:
            return bars
        else:
            return bars[[fields]]

    # TODO: To be implemented
    def current_snapshot(self, instrument, frequency, dt):
        raise NotImplementedError

    def get_yield_curve(self, start_date, end_date, tenor=None):
        return self._yield_curve.get_yield_curve(start_date, end_date, tenor)

    def get_risk_free_rate(self, start_date, end_date):
        return self._yield_curve.get_risk_free_rate(start_date, end_date)

    def get_split(self, order_book_id):
        return None

    # TODO: To be implemented
    def is_suspended(self, order_book_id, dt):
        return False

    # TODO: To be implemented
    def is_st_stock(self, order_book_id, dt):
        return False

    @lru_cache(None)
    def get_instruments_from_mongo(self):
        instruments = []
        codes_cursor = self.db[INSTRUMENT_COL].find().sort("windCode", pymongo.ASCENDING)
        for doc in codes_cursor:
            instrument_dict = {
                'industry_name': 'UNKNOWN',
                'symbol': doc['name'],
                'sector_code': 'UNKNOWN',
                'special_type': 'Normal',
                'industry_code': 'UNKNOWN',
                'type': 'CS',
                'listed_date': '2014-06-01',
                'de_listed_date': '0000-00-00',
                'status': 'Active',
                'concept_names': 'null',
                'abbrev_symbol': 'UNKNOWN',
                'round_lot': 100.0,
                'board_type': 'UNKNOWN',
                'exchange': doc['windCode'].split('.')[1],
                'order_book_id': doc['windCode'],
                'sector_code_name': 'UNKNOWN'}
            instruments.append(Instrument(instrument_dict))
        return instruments

    @lru_cache(None)
    def get_trading_dates_from_mongo(self, code):
        trading_dates = []
        cursor = self.db[get_col_name(code)].find(
            {'cycType': CycType.CYC_DAY}, {'_id': False, 'date': True}).sort("date", pymongo.ASCENDING)
        for doc in cursor:
            trading_dates.append(doc['date'])
        return pd.Index(pd.Timestamp(d) for d in trading_dates)

    @lru_cache(None)
    def get_stock_data_from_mongo(self, code, cyc_type, datetime):
        """
        :param str code: WindCode
        :param cyc_type: Type from CycType
        :param datetime.datetime datetime: Current datetime
        :return: numpy.ndarray
        """
        mongo_doc = self.db[get_col_name(code)].find_one({'date': datetime, 'cycType': cyc_type})
        if mongo_doc is None:
            return None
        dtype = np.dtype([(f, FIELDS[f]) for f in FIELDS.keys()])
        bar = np.zeros(shape=(), dtype=dtype)
        bar['datetime'] = convert_date_to_int(datetime)
        bar['open'] = mongo_doc['open']
        bar['close'] = mongo_doc['close']
        bar['high'] = mongo_doc['high']
        bar['low'] = mongo_doc['low']
        bar['volume'] = mongo_doc['volume']
        bar['total_turnover'] = mongo_doc['amount']
        return bar

    @lru_cache(None)
    def get_stock_data_hist_from_mongo(self, code, cyc_type, datetime, bar_count):
        """
        :param str code: WindCode
        :param cyc_type: Type from CycType
        :param datetime.datetime datetime: Current datetime
        :param int bar_count: Required history bar count
        :return: numpy.ndarray
        """
        cursor = self.db[get_col_name(code)].find(
            {'cycType': cyc_type, 'date': {"$lte": datetime}}).sort("date", pymongo.ASCENDING).limit(bar_count)

        if cursor.count() < bar_count:
            raise DataFeedError('Required bar_count: {} > found docs: {}'.format(bar_count, cursor.count()))

        dtype = np.dtype([(f, FIELDS[f]) for f in FIELDS.keys()])
        bars = np.zeros(shape=(bar_count,), dtype=dtype)
        i = 0
        for doc in cursor:
            bars[i]['datetime'] = convert_date_to_int(datetime)
            bars[i]['open'] = doc['open']
            bars[i]['close'] = doc['close']
            bars[i]['high'] = doc['high']
            bars[i]['low'] = doc['low']
            bars[i]['volume'] = doc['volume']
            bars[i]['total_turnover'] = doc['amount']
            i += 1
        return bars

    @staticmethod
    def _are_fields_valid(fields, valid_fields):
        if fields is None:
            return True
        for field in fields:
            if field not in valid_fields:
                return False
        return True

    def get_future_info(self, instrument, hedge_type):
        raise NotImplementedError

    def get_trading_minutes_for(self, order_book_id, trading_dt):
        """
        Get future trading time in one day
        """
        raise NotImplementedError

    def get_settle_price(self, instrument, date):
        """
        Get future settle price in date
        """
        raise NotImplementedError
