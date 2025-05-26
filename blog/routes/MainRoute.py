from flask import Blueprint
from blog.controllers import MainController, AuthController




"""For The Main Controller """

MainRoute = Blueprint("MainRoute", __name__)

MainRoute.route('/')(MainController.home)






"""For The Auth Controller """

AutherRoute = Blueprint("AuthRoute", __name__, url_prefix='/auth')


AutherRoute.route('/login', methods=['POST', 'GET'])(AuthController.user_login)
AutherRoute.route('/register', methods=['POST', 'GET'])(AuthController.user_register)
AutherRoute.route('/logout', methods=['GET'])(AuthController.user_logout)
AutherRoute.route('/reset_password', methods=['POST', 'GET'])(AuthController.reset_request)
AutherRoute.route('/reset_password/<token>', methods=['POST', 'GET'])(AuthController.reset_password)



"""For The Subscribe Controller """

SubscribeRoute = Blueprint("SubscribeRoute", __name__, url_prefix='/subscribe')






"""For The Article Controller """

ArticleRoute = Blueprint("ArticleRoute", __name__, url_prefix='/article')


ArticleRoute.route('/add', methods=['POST', 'GET'])(MainController.article_add)



