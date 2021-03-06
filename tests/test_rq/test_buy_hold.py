from rqalpha import run
from rqalpha.api import *
from rqalpha.utils.datetime_func import convert_int_to_datetime


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "000001.SZ"
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False


def before_trading(context):
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    logger.info(bar_dict[context.s1])

    prices = history_bars(context.s1, 3, '1d', ['datetime', 'close'])
    logger.info([x for x in prices])

    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 1)
        context.fired = True


if __name__ == '__main__':
    from ialgotest.conf.generate_config import gen_conf

    run(gen_conf(__file__))
