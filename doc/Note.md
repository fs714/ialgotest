### Change rqalpha lib as below

data/instrument_mixin.py:        # Updated by [Sfang]
data/instrument_mixin.py-        # 沪深300 中证500 固定使用上证的
data/instrument_mixin.py-        # for o in ['000300.XSHG', '000905.XSHG']:
data/instrument_mixin.py-        #     self._sym_id_map[self._instruments[o].symbol] = o
data/instrument_mixin.py-        # 上证180 及 上证180指数 两个symbol都指向 000010.XSHG
data/instrument_mixin.py-        # self._sym_id_map[self._instruments['SSE180.INDX'].symbol] = '000010.XSHG'
--
api/api_stock.py:        # Update by [Sfang]
api/api_stock.py-        if "SH" in order_book_id or "SZ" in order_book_id:
api/api_stock.py-            return order_book_id
api/api_stock.py-        else:
