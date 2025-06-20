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
    MEDIA_DIR  = APP_DIR / 'static' /  "media"
    IMAGES_DIR = MEDIA_DIR / "images"


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


    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PORT = 2525
    EMAIL_TIMEOUT = 30
    EMAIL_USE_TLS = True 
    EMAIL_USE_SSL = False 
    
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_API_VERSION = os.environ.get("STRIPE_API_VERSION")
    STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

    PRICES = {
    'MONTHLY_SUBSCRIPTION_ID' : os.environ.get('MONTHLY_SUBSCRIPTION_ID'),
    'YEARLY_SUBSCRIPTION_ID' : os.environ.get('YEARLY_SUBSCRIPTION_ID')
    }

    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    #postgreSQL conf
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEFAULT_ARTICLE_IMAGE = 'default.png'

    ARTICLES_PER_PAGE = 9
    RECORD_PER_PAGE = 21


    LOGIN_MESSAGE = "Login Required"




class ProductionConfig(Config):
    pass