import os
from dotenv import load_dotenv
from flask_mail import Mail, Message
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    UPLOAD_FOLDER = './static'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.environ.get('SENDGRID_API_KEY')
    ADMINS = ['email']
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    POSTS_PER_PAGE = 25
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    WTF_CSRF_ENABLED = False