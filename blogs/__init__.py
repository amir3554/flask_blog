from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from blog.config import DevelopmentConfig, ProductionConfig


""" Development Mode """
conf = DevelopmentConfig()

""" Production Mode """
#conf = ProductionConfig()


"""Initiating Libraris Objects"""

bcrypt = Bcrypt()

db = SQLAlchemy()

migrate = Migrate()

flask_seeder = FlaskSeeder()


""" this function for creating the app """
def create_app() -> Flask:
    app = Flask(__name__, template_folder=conf.VIEWS_DIR, static_folder=conf.STATIC_DIR,)
    
    app.config.from_object(conf)

    with app.app_context():

        register_extention(app)
        
        register_blueprint(app)
        
        app.before_request(populate_database)

    return app



def register_extention(app : Flask) -> None:
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    flask_seeder.init_app(app, db)
    return None


def register_blueprint(app : Flask) -> None:
    from blog.routes import MainRoute
    app.register_blueprint(MainRoute.MainRoute)
    app.register_blueprint(MainRoute.ArticleRoute)
    app.register_blueprint(MainRoute.AutherRoute)
    app.register_blueprint(MainRoute.SubscribeRoute)
    return None



from blog.models.Models import Article, User, StripeCustomer, Like


def populate_database() -> None:
    db.create_all()
    user = User.query.filter_by(username=conf.OWNER_USERNAME).first()
    if user is None:
        user = User(
            username=conf.OWNER_USERNAME, 
            email=conf.OWNER_EMAIL, 
            password = bcrypt.generate_password_hash(conf.OWNER_PASSWORD).decode("utf-8"),
            first_name = conf.OWNER_FIRSTNAME,
            last_name = conf.OWNER_LASTNAME,
            is_admin = True 
            )
    db.session.add(user)
    db.session.commit()

    return None