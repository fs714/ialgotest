from rqalpha.interface import AbstractMod

from ...data_feeds.rqalpha_mongo_data_source import MongoDataSource


class MongoFeedMod(AbstractMod):
    def start_up(self, env, mod_config):
        env.set_data_source(MongoDataSource(mod_config.mongo_ip, mod_config.mongo_port, mod_config.mongo_db_name))

    def tear_down(self, code, exception=None):
        pass
