from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_login import LoginManager
from flask_mail import Mail
from blog.config import DevelopmentConfig, ProductionConfig
from datetime import datetime

""" Development Mode """
conf = DevelopmentConfig()

""" Production Mode """
#conf = ProductionConfig()


"""Initiating Libraris Objects"""

bcrypt = Bcrypt()

db = SQLAlchemy()

migrate = Migrate()

flask_seeder = FlaskSeeder()

login_manager = LoginManager()

mail = Mail()


login_manager.login_view = "auth_controller.user_login" #type:ignore
login_manager.login_message = conf.LOGIN_MESSAGE
login_manager.login_message_category = "warning"


""" this function for creating the app """
def create_app() -> Flask:
    app = Flask(__name__, template_folder=conf.VIEWS_DIR, static_folder=conf.STATIC_DIR,)
    
    app.config.from_object(conf)

    with app.app_context():

        register_extention(app)
        
        register_blueprint(app)

        register_error_handler(app)
        

        (app.context_processor)(inject_now)

    return app



def register_extention(app : Flask) -> None:
    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    flask_seeder.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
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
    #app.before_request(populate_database)
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


def register_error_handler(app):
    def render_error(error):
        error_code = getattr(error, "code", 404)
        return render_template(
            f"main/{error_code}.html",
            error_code=error_code,
            title="Not Found",
            ),error_code
    
    for errcode in [404]:
        app.errorhandler(errcode)(render_error)
    
    return None

def inject_now() -> dict:
    return { "now" : datetime.utcnow().year }


@login_manager.user_loader
def load_user(user_id : int) -> object | None:
    # هنا ترجع مثيلاً من User أو None
    return User.query.get(int(user_id))


