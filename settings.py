
user = 'saying'
password = 'saying'
hostname = '127.0.0.1'
dbname = 'diantea'

class Config:
    DEBUG = True
    use_reloader=False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/{}?charset=utf8'.format(user, password, hostname, dbname)
    JWT_SECRET = 'saying'
    JWT_EXPIRATION_DELTA = 3600 * 1000
    SECRET_KEY = 'saying'