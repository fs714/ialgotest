from __future__ import (absolute_import, division, print_function, unicode_literals)

import datetime as dt

import backtrader as bt
import backtrader.feed as feed
from backtrader.utils import date2num
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure


def get_col_name(code):
    """
    :type code str
    """
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


TIMEFRAMES = dict(
    (
        (bt.TimeFrame.Minutes, CycType.CYC_MINUTE),
        (bt.TimeFrame.Days, CycType.CYC_DAY),
        (bt.TimeFrame.Weeks, CycType.CYC_WEEK),
        (bt.TimeFrame.Months, CycType.CYC_MONTH),
        (bt.TimeFrame.Years, CycType.CYC_YEAR),
    )
)


class MongoFeed(feed.DataBase):
    lines = (('turn'), ('transNum'),)

    params = (
        ('host', '127.0.0.1'),
        ('port', 27017),
        ('username', None),
        ('password', None),
        ('database', None),
        ('code', None),
        ('timeframe', bt.TimeFrame.Days),
        ('fromdate', dt.datetime(1970, 1, 1, 0, 0, 0, 0)),
        ('todate', dt.datetime.now()),
    )

    def start(self):
        super(MongoFeed, self).start()

        self.client = MongoClient(self.p.host, self.p.port)
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
        except ConnectionFailure as err:
            print('Failed to establish connection to MongoDB: %s' % err)

        self.db = self.client[self.p.database]
        self.col = self.db[get_col_name(self.p.code)]

        cyc_type = TIMEFRAMES.get(self.p.timeframe)

        bars_db = self.col.find({'cycType': cyc_type,
                                 'date': {"$gte": self.p.fromdate, "$lte": self.p.todate}}).sort("date", ASCENDING)
        self.bars_iter = iter(bars_db)

    def _load(self):
        try:
            bar = next(self.bars_iter)
        except StopIteration:
            return False

        self.l.datetime[0] = date2num(bar['date'])
        self.l.open[0] = bar['open']
        self.l.high[0] = bar['high']
        self.l.low[0] = bar['low']
        self.l.close[0] = bar['close']
        self.l.volume[0] = bar['volume']
        self.l.turn[0] = bar['turn'] or -1
        self.l.transNum[0] = bar['transNum'] or -1

        return True
