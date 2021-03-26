import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    MAIL_SERVER = str(os.environ.get("MAIL_SERVER"))
    MAIL_PORT = str(os.environ.get("MAIL_PORT"))
    MAIL_USERNAME = str(os.environ.get("MAIL_USERNAME"))
    MAIL_PASSWORD = str(os.environ.get("MAIL_PASSWORD"))
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    JWT_SECRET_KEY = str(os.environ.get("JWT_SECRET"))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True