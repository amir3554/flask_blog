import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


class Config():
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    DEBUG = True
    APP_DIR = Path(os.path.dirname(os.path.realpath(__file__)))
    CONTROLLER_DIR = APP_DIR / "controller"
    VIEWS_DIR  = APP_DIR /  "template"
    MODELS_DIR = APP_DIR / "models"
    ROUTES_DIR = APP_DIR / "routes"
    STATIC_DIR = APP_DIR / "static"
    MEDIA_DIR  = APP_DIR /  "media"

    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    #postgreSQL conf
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False




class ProductionConfig(Config):
    pass