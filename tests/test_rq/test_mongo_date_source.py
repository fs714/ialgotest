from datetime import datetime

from ialgotest.data_feeds.rqalpha_mongo_data_source import MongoDataSource

if __name__ == '__main__':
    data_src = MongoDataSource()
    instruments = data_src.get_all_instruments()
    instrument = None
    for i in instruments:
        if i.order_book_id == '600000.SH':
            instrument = i

    bar = data_src.get_bar(instrument, datetime(2017, 3, 15), '1d')
    print(bar)
