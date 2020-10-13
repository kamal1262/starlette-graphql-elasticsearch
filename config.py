import os
import databases
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


config = Config(".env")
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    APP_TITLE = config("TITLE", default="API")
    JWT_SECRET_KEY = config("JWT_SECRET_KEY", cast=Secret)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = int(config("SQLALCHEMY_POOL_RECYCLE", default=3600))
    LOG_FORMAT = "[%(asctime)s] %(module)s - %(levelname)s: %(message)s"
    LOG_LEVEL = config("LOG_LEVEL", default="INFO")
    ERROR_404_HELP = False
    SWAGGER = {
        "title": config("TITLE", default="API"),
        "version": config("VERSION", default="Undefined"),
        "uiversion": 3,
        "openapi": "3.0.2",
        "specs": [{"endpoint": "apispec", "route": "/apispec.json"}],
    }
    XRAY = {
        "enabled": (config("XRAY_ENABLED", default="False") or "False").lower()
        == "true",
        "daemon_url": config("XRAY_DAEMON_URL", default="127.0.0.1:2000"),
        "inspect_sql_query": config("XRAY_INSPECT_QUERY", default="False"),
    }
    JWT_ACCESS_TOKEN_EXPIRES = False
    SQLALCHEMY_DATABASE_URI = config("DATABASE_URI", cast=databases.DatabaseURL)
    MESSAGE_PRODUCER = config("PRODUCER_TYPE", default="")
    MESSAGE_TOPICS = config("PRODUCER_TOPICS", default="", cast=CommaSeparatedStrings)
    TOPIC_CONSUMERS = config("TOPIC_CONSUMERS", default="", cast=CommaSeparatedStrings)
    TOPIC_INTERVAL = int(config("TOPIC_INTERVAL", default="30"))


class ProductionConfig(BaseConfig):
    ENV = "production"


class DevelopmentConfig(BaseConfig):
    ENV = "development"


class TestConfig(BaseConfig):
    ENV = "test"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "TeStKey"
