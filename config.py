import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = True
    QUERY_LIMIT = 15000
    SECRET_KEY = os.urandom(64)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + BASE_DIR + "/db.sqlite3"
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    APP_NAME = "SEQUEL: DB Workload Runner"
    API_KEY = "?key="
    BASE_URL = "https://my.api.mockaroo.com/"


class DevelopmentConfig(Config):
    QUERY_LIMIT = 10000


class ProductionConfig(Config):
    QUERY_LIMIT = 100000


class DockerConfig(Config):
    QUERY_LIMIT = 5000


config = {
    "development": DevelopmentConfig(),
    "production": ProductionConfig(),
    "docker": DockerConfig()
}






