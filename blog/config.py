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
    VIEWS_DIR  = APP_DIR /  "views"
    MODELS_DIR = APP_DIR / "models"
    ROUTES_DIR = APP_DIR / "routes"
    STATIC_DIR = APP_DIR / "static"
    MEDIA_DIR  = APP_DIR /  "media"
    TEMPLATES_DIR = APP_DIR / "templates"

class ProductionConfig(Config):
    pass