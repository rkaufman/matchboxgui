import os
DATABASE = os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), 'mxedgesql.db')

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secretkey')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = DATABASE

class ProductionConfig(BaseConfig):
    SECRET_KEY = 'prodkey'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = DATABASE