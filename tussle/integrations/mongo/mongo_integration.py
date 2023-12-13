from pymongo.mongo_client import MongoClient
import os
from tussle.general.config.config import load_cloud_configuration
from tussle.general.logger import get_logger

db = None
logger = get_logger('mongo')
dbs_by_alias = {}


def load_db_connection_settings(config=None):
    if config is None:
        config = load_cloud_configuration()

    mongo_uri = config['db']['mongo_uri']
    username = config['db']['username']
    password = config['db']['password']
    db_name = config['db']['db_name']

    if os.environ.get('MONGO_DATABASE_NAME_SUFFIX'):
        db_name += os.environ['MONGO_DATABASE_NAME_SUFFIX']

    return mongo_uri, username, password, db_name


def connect_to_database_pymongo(config=None, alias='default'):
    global dbs_by_alias
    global db

    if dbs_by_alias.get(alias) is not None:
        logger.info(f"Returning existing database connection for alias '{alias}'")
        return dbs_by_alias[alias]

    mongo_uri, username, password, db_name = load_db_connection_settings(config)

    logger.info(f"Connecting to database '{db_name}' at '{mongo_uri}' with pymongo, and assigning it to alias '{alias}'")
    db = MongoClient(mongo_uri, username=username, password=password)[db_name]

    dbs_by_alias[alias] = db

    return db
