import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


class Config():
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    APP_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
    CONTROLLER_DIR = APP_DIR / "controller"
    VIEWS_DIR  = APP_DIR /  "template"
    MODELS_DIR = APP_DIR / "models"
    ROUTES_DIR = APP_DIR / "routes"
    STATIC_DIR = APP_DIR / "static"
    MEDIA_DIR  = APP_DIR /  "media"


    OWNER_FIRSTNAME = os.environ.get('OWNER_FIRSTNAME')
    OWNER_LASTNAME = os.environ.get('OWNER_LASTNAME')
    OWNER_EMAIL = os.environ.get('OWNER_EMAIL')
    OWNER_USERNAME = os.environ.get('OWNER_USERNAME')
    OWNER_PASSWORD = os.environ.get('OWNER_PASSWORD')

    # seed faker info
    ACCOUNT_COUNT = 25
    USER_PASSWORD = 'user123'
    ADMIN_PERCENTAGE = 10 #10%
    ARTICLE_COUNT = 100
    CUSTOMER_COUNT = 20
    START_DATE = datetime(2025, 1, 25)
    LIKES_COUNT = 500


    MAIL_SERVER = os.environ['MAIL_SERVER']
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_PORT = 2525
    EMAIL_TIMEOUT = 30
    EMAIL_USE_TLS = True 
    EMAIL_USE_SSL = False 

    # MAIL_SERVER = 'sandbox.smtp.mailtrap.io'
    # MAIL_USERNAME = 'f73c57ad7e6649'
    # MAIL_PASSWORD = 'b8bd177a9f4af9'

    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    #postgreSQL conf
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    LOGIN_MESSAGE = "Login Required"




class ProductionConfig(Config):
    pass