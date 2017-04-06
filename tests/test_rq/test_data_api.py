from rqalpha import run
from rqalpha.api import *


def init(context):
    context.s1 = "000001.SZ"
    logger.info(context.run_info)
    logger.info('-- {} --'.format(context.universe))
    # logger.info(all_instruments(type='CS'))
    logger.info(instruments('000001.XSHE'))
    logger.info(instruments(['000001.XSHE', '000002.XSHE']))
    # Get stock list in one industry
    logger.info('Industry: {}'.format(industry('C34')))
    logger.info('Sector: {}'.format(sector('TelecommunicationServices')))
    logger.info('Concept: {}'.format(concept('民营医院', '国企改革')))
    # logger.info('Devidend:\n{}'.format(get_dividend('000001.XSHE', start_date='20130104')))
    logger.info('Trade Dates: {}'.format(get_trading_dates(start_date='2016-05-01', end_date='20160505')))
    logger.info('Previous Trade Date: {}'.format(get_previous_trading_date(date='2016-05-02')))
    logger.info('Next Trade Date: {}'.format(get_next_trading_date(date='2016-05-02')))
    logger.info('Yield Curve: {}'.format(get_yield_curve('20130104')))


def handle_bar(context, bar_dict):
    # Get contract pool
    # logger.info(context.universe)

    # Use bar_dict[order_book_id] to get the bar info
    # logger.info(bar_dict[context.s1])

    # Use context.portfolio to get investment portfolio till now
    # logger.info(context.portfolio)
    # logger.info(context.portfolio.cash)
    # logger.info(context.portfolio.positions[context.s1].quantity)

    # Calculate current position in portfolio
    # cur_position = context.portfolio.positions[context.s1].quantity
    # Calculte how many stocks we can buy with all available cash
    # shares = context.portfolio.cash / bar_dict[context.s1].close
    # logger.info(shares)

    # Use history_bars to get history bars as list
    # logger.info(history_bars(context.s1, 5, '1d', 'close'))

    # Get current snapshot
    # logger.info(current_snapshot(context.s1))

    # 使用order_shares(id_or_ins, amount)方法进行落单

    pass


if __name__ == '__main__':
    from ialgotest.conf.generate_config import gen_conf

    run(gen_conf(__file__))
