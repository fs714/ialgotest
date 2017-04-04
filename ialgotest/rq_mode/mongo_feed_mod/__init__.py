__config__ = {
    'mongo_ip': '127.0.0.1',
    'mongo_port': 27017,
    'mongo_db_name': 'emquant'
}


def load_mod():
    from .mod import MongoFeedMod
    return MongoFeedMod()
