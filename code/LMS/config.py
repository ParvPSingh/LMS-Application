import os

curr_dir=os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///"+os.path.join(curr_dir, "local_db.sqlite3")
    SECRET_KEY = "thisissecter"
    SECURITY_PASSWORD_SALT = "thisissaltt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
    CACHE_TYPE = "RedisCache"
    #CACHE_REDIS_HOST = "localhost"
    #CACHE_REDIS_PORT = 6379
    #CACHE_REDIS_DB = 3
    CACHE_REDIS_URL = "redis://localhost:6379/3"
    CACHE_DEFAULT_TIMEOUT = 300