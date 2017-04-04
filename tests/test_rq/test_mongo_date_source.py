from datetime import datetime

from ialgotest.data_feeds.rqalpha_mongo_data_source import MongoDataSource

if __name__ == '__main__':
    data_src = MongoDataSource()

    instruments = data_src.get_all_instruments()
    print('-' * 6 + 'Instruments' + '-' * 6)
    print([i.order_book_id for i in instruments])

    instrument = None
    for i in instruments:
        if i.order_book_id == '600000.SH':
            instrument = i

    print('-' * 6 + 'Trading Calendar' + '-' * 6)
    print(data_src.get_trading_calendar())

    print('-' * 6 + 'Available Data Range' + '-' * 6)
    print(data_src.available_data_range('1d'))

    bar = data_src.get_bar(instrument, datetime(2017, 3, 15), '1d')
    print(bar)

    bars = data_src.history_bars(instrument, 10, '1d', None, datetime(2016, 8, 1))
    print(bars)
