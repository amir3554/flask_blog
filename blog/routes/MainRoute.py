from flask import Blueprint
from blog.controllers.MainController import MainController

MainRoute = Blueprint("main_controller", __name__)

MainRoute.route('/')(MainController.home)