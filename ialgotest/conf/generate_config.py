def gen_conf(strategy_file, freq='1d', start='2015-01-01', end='2016-01-01', plot=False, save_plot=False,
             save_output=False, report_path=None, mongo_feed=True):
    config = {
        'version': '0.1.5',
        # 白名单，设置可以直接在策略代码中指定哪些模块的配置项目
        'whitelist': ['base', 'extra', 'validator', 'mod'],
        'base': {
            # 启动的策略文件路径
            'strategy_file': strategy_file,
            # 数据源所存储的文件路径
            'data_bundle_path': '/root/.rqalpha/bundle',
            # 回测起始日期
            'start_date': start,
            # 回测结束日期(如果是实盘，则忽略该配置)
            'end_date': end,
            # 目前支持 `1d` (日线回测) 和 `1m` (分钟线回测)
            'frequency': freq,
            # 股票起始资金
            'stock_starting_cash': 100000.0,
            # 期货起始资金
            'future_starting_cash': 0,
            # 设置保证金乘数，默认为1
            'margin_multiplier': 1,
            # Benchmark，如果不设置，默认没有基准参照
            # 'benchmark': '000300.XSHG',
            'benchmark': '600000.SH',
            # 运行类型，`b` 为回测，`p` 为模拟交易, `r` 为实盘交易
            'run_type': 'b',
            # 设置策略可交易品种，目前支持 `stock` (股票策略)、`future` (期货策略)tst
            'securities': ['stock'],
            # 在模拟交易和实盘交易中，RQAlpha支持策略的pause && resume，该选项表示开启 resume 功能
            'resume_mode': False,
            # 在模拟交易和实盘交易中，该选项表示开启 persist功能，其会在每个bar结束对进行策略的持仓、账户信息，用户的代码上线文等内容进行持久化
            'persist': False,
            'persist_mode': 'real_time',
            # 选择是否开启自动处理, 默认不开启
            'handle_split': False
        },
        'extra': {
            # 选择日期的输出等级，有 `verbose` | `info` | `warning` | `error`
            'log_level': 'info',
            'locale': 'cn',
            'user_system_log_disabled': False,
            'context_vars': None,
            'force_run_init_when_pt_resume': False,
            # enable_profiler: 是否启动性能分析
            'enable_profiler': False,
            'is_hold': False
        },
        'validator': {
            # 开启该项，当持仓股票退市时，按照退市价格返还现金
            'cash_return_by_stock_delisted': False,
            # 在执行order_value操作时，进行实际下单数量的校验和scale
            'close_amount': True
        },
        'mod': {
            'sys_simulation': {
                'enabled': True,
                'commission_multiplier': 1.0,
                'slippage': 0.0,
                'matching_type': 'next_bar',
                'signal': False
            },
            'sys_analyser': {
                'enabled': True,
                'output_file': (strategy_file.split('.')[0] + '.output') if save_output else None,
                'plot': plot,
                'plot_save_file': (strategy_file.split('.')[0] + '_plot') if save_plot else None,
                'report_save_path': report_path
            },
            'sys_progress': {
                'enabled': True,
                'show': False
            },
            'sys_risk': {
                'enabled': True,
                'validate_position': True
            },
            'mongo_feed': {
                'enabled': mongo_feed,
                'lib': 'ialgotest.rq_mode.mongo_feed_mod'
            },
            'sys_stock_realtime': {
                'enabled': False
            },
            'sys_funcat': {
                'enabled': False
            }
        }
    }
    return config
