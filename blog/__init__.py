from flask import Flask
from flask_bcrypt import Bcrypt
from blog.config import DevelopmentConfig, ProductionConfig


""" Development Mode """
conf = DevelopmentConfig()

""" Production Mode """
#conf = ProductionConfig()

bcrypt = Bcrypt()

""" this function for creating the app """
def create_app():
    app = Flask(__name__,
                template_folder=conf.VIEWS_DIR,
                static_folder=conf.STATIC_DIR,
                )
    
    

