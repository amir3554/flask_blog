from flask import Blueprint
from blog.controllers.MainController import MainController

MainRoute = Blueprint("main_controller", __name__)

MainRoute.route('/')(MainController.home)

SubscribeRoute = Blueprint("subscribe_controller", __name__, url_prefix='/subscribe')

AutherRoute = Blueprint("auther_controller", __name__, url_prefix='/auther')

ArticleRoute = Blueprint("article_controller", __name__, url_prefix='/article')
