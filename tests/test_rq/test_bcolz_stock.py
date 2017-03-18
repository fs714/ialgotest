import bcolz
import numpy as np


def field_type(c_dtyep, field, dt_orig):
    try:
        return c_dtyep[field][0]
    except KeyError:
        return dt_orig


float64 = np.dtype('float64')

cdtype = {
    'open': (float64, 1 / 10000.0, 4),
    'close': (float64, 1 / 10000.0, 4),
    'high': (float64, 1 / 10000.0, 4),
    'low': (float64, 1 / 10000.0, 4),
    'limit_up': (float64, 1 / 10000.0, 4),
    'limit_down': (float64, 1 / 10000.0, 4),
}

if __name__ == '__main__':
    bc = bcolz.open('/home/eshufan/project/bundle/stocks.bcolz', 'r')

    # Access /home/eshufan/project/bundle/stocks.bcolz/__attrs__
    se = bc.attrs['line_map']
    print('Get the lines for 600000.XSHG')
    s, e = se['600000.XSHG']
    print('Start from {}, end to {}'.format(s, e))

    print('Get all column names')
    print(bc.names)
    print('Exclude the first column for date')
    fields = bc.names[1:]
    print(fields)

    print('Print original data type for each column')
    print([bc.cols[f].dtype for f in fields])

    print('Construct the data type for each column')
    dtype = np.dtype([('datetime', np.uint64)] + [(f, field_type(cdtype, f, bc.cols[f].dtype)) for f in fields])
    print(dtype)

    print('Create an empty numpy list with random valume, size is row: e - s, column: len(dtype) (Include datetime)')
    result = np.empty(shape=(e - s,), dtype=dtype)

    print('Feed the real data')
    for f in fields:
        result[f][:] = bc.cols[f][s:e]
    print(result)

    print('Update column datetime')
    result['datetime'][:] = bc.cols['date'][s:e].astype(np.uint64) * 1000000
    print(result)
