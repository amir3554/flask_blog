from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from blog.config import DevelopmentConfig, ProductionConfig


""" Development Mode """
conf = DevelopmentConfig()

""" Production Mode """
#conf = ProductionConfig()

bcrypt = Bcrypt()

db = SQLAlchemy()

migrate = Migrate()

""" this function for creating the app """
def create_app():
    app = Flask(__name__,
                template_folder=conf.VIEWS_DIR,
                static_folder=conf.STATIC_DIR,
                )
    
    app.config.from_object(conf)
    with app.app_context():
        bcrypt.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)

        from blog.routes import MainRoute, ArticleRouter, AuthRouter, SubscribeRouter
        app.register_blueprint(MainRoute.MainRoute)
        app.register_blueprint(ArticleRouter.ArticleRoute)
        app.register_blueprint(AuthRouter.AutherRoute)
        app.register_blueprint(SubscribeRouter.SubscribeRoute)


    return app


from blog.models.ArticleModel import Article
from blog.models.LikeModel import Like
from blog.models.SubscribeModel import StripeCustomer
from blog.models.UserModel import User