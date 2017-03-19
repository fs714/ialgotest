def gen_conf(strategy_file):
    config = {
        'whitelist': ['base', 'extra', 'validator', 'mod'],
        'base': {
            'run_id': 9999,
            'strategy_file': strategy_file,
            'data_bundle_path': '/root/.rqalpha/bundle',
            'start_date': '2014-01-01',
            'end_date': '2016-01-01',
            'frequency': '1d',
            'stock_starting_cash': 100000.0,
            'future_starting_cash': 0,
            'commission_multiplier': 1,
            'margin_multiplier': 1,
            'slippage': 0,
            'benchmark': '000001.XSHE',
            'run_type': 'b',
            'strategy_type': 'stock',
            'matching_type': 'current_bar',
            'resume_mode': False,
            'persist': False,
            'persist_mode': 'real_time',
            'handle_split': False
        },
        'extra': {
            'log_level': 'verbose',
            'locale': 'cn',
            'user_system_log_disabled': False,
            'context_vars': None,
            'force_run_init_when_pt_resume': False,
            'enable_profiler': False,
            'is_hold': False
        },
        'validator': {
            'cash_return_by_stock_delisted': False,
            'close_amount': True,
            'bar_limit': True
        },
        'mod': {
            'simulation': {
                'lib': 'rqalpha.mod.simulation',
                'enabled': True,
                'priority': 100
            },
            'funcat_api': {
                'lib': 'rqalpha.mod.funcat_api',
                'enabled': False,
                'priority': 200
            },
            'progress': {
                'lib': 'rqalpha.mod.progress',
                'enabled': False,
                'priority': 400
            },
            'simple_stock_realtime_trade': {
                'lib': 'rqalpha.mod.simple_stock_realtime_trade',
                'persist_path': './persist/strategy/',
                'fps': 3,
                'enabled': False,
                'priority': 500
            },
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
                'available_cash': True,
                'available_position': True,
                'short_stock': False
            },
            'analyser': {
                'priority': 100,
                'enabled': True,
                'lib': 'rqalpha.mod.analyser',
                'record': True,
                'output_file': None,
                'plot': True,
                'plot_save_file': strategy_file.split('.')[0] + '_plot',
                'report_save_path': None
            }
        },
        'version': '0.1.2'
    }
    return config
