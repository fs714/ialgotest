def gen_conf(strategy_file, plot=False, save_plot=False, save_output=False, report_path=None):
    config = {
        'whitelist': ['base', 'extra', 'validator', 'mod'],
        'base': {
            'run_id': 9999,
            'strategy_file': strategy_file,
            'data_bundle_path': '/root/.rqalpha/bundle',
            'start_date': '2014-01-01',
            'end_date': '2016-01-01',
            # 目前支持 `1d` (日线回测) 和 `1m` (分钟线回测)
            'frequency': '1d',
            # 股票起始资金
            'stock_starting_cash': 100000.0,
            # 期货起始资金
            'future_starting_cash': 0,
            # 设置手续费乘数，默认为1
            'commission_multiplier': 1,
            # 设置保证金乘数，默认为1
            'margin_multiplier': 1,
            # 设置滑点
            'slippage': 0,
            # Benchmark，如果不设置，默认没有基准参照
            'benchmark': '000001.XSHE',
            # 运行类型，`b` 为回测，`p` 为模拟交易, `r` 为实盘交易
            'run_type': 'b',
            # 设置策略类型，目前支持 `stock` (股票策略)、`future` (期货策略)及 `stock_future` (混合策略)
            'strategy_type': 'stock',
            # 启用的回测引擎，目前支持 `current_bar` (当前Bar收盘价撮合) 和 `next_bar` (下一个Bar开盘价撮合)
            'matching_type': 'current_bar',
            'resume_mode': False,
            'persist': False,
            'persist_mode': 'real_time',
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
            'close_amount': True,
            # 在处于涨跌停时，无法买进/卖出
            'bar_limit': True
        },
        'mod': {
            # 回测 / 模拟交易 支持 Mod
            'simulation': {
                'lib': 'rqalpha.mod.simulation',
                'enabled': True,
                'priority': 100
            },
            # 技术分析API
            'funcat_api': {
                'lib': 'rqalpha.mod.funcat_api',
                'enabled': False,
                'priority': 200
            },
            # 开启该选项，可以在命令行查看回测进度
            'progress': {
                'lib': 'rqalpha.mod.progress',
                'enabled': False,
                'priority': 400
            },
            # 接收实时行情运行
            'simple_stock_realtime_trade': {
                'lib': 'rqalpha.mod.simple_stock_realtime_trade',
                'persist_path': './persist/strategy/',
                'fps': 3,
                'enabled': False,
                'priority': 500
            },
            # 渐进式输出运行结果
            'progressive_output_csv': {
                'lib': 'rqalpha.mod.progressive_output_csv',
                'enabled': False,
                'output_path': './',
                'priority': 600
            },
            'risk_manager': {
                'lib': 'rqalpha.mod.risk_manager',
                'enabled': True,
                'priority': 700,
                # available_cash: 查可用资金是否充足，默认开启
                'available_cash': True,
                # available_position: 检查可平仓位是否充足，默认开启
                'available_position': True,
                # 允许裸卖空
                'short_stock': False
            },
            'analyser': {
                'priority': 100,
                'enabled': True,
                'lib': 'rqalpha.mod.analyser',
                'record': True,
                'output_file': (strategy_file.split('.')[0] + '.output') if save_output else None,
                'plot': plot,
                'plot_save_file': (strategy_file.split('.')[0] + '_plot') if save_plot else None,
                'report_save_path': report_path
            }
        },
        'version': '0.1.2'
    }
    return config
