from blog import db, conf
from sqlalchemy.sql import func
from flask_login import UserMixin
from itsdangerous.url_safe import URLSafeSerializer



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    first_name = db.Column(db.String(30), nullable=False, unique=False)
    last_name = db.Column(db.String(30), nullable=False, unique=False)
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False, unique=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    articles = db.relationship("Article", backref='user', lazy=True)
    stripe_customer = db.relationship("StripeCustomer", backref='user')
    likes = db.relationship('Like', backref='user', passive_deletes=True)

    def get_reset_pwd_token(self) -> str:
        sign = URLSafeSerializer(conf.SECRET_KEY, salt="PasswordReset") #type:ignore
        return sign.dumps({ 'user_id' : self.id })
    
    @staticmethod
    def verify_reset_pwd_token(token : str) -> object | None :
        sign = URLSafeSerializer(conf.SECRET_KEY, salt="PasswordReset") #type:ignore
        try:
            user_id = sign.loads(token, max_age=3600)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"User ('{self.username}' . '{self.email}')"
    


class StripeCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    subscription_type = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="RESTRIC"))
    subscription_id = db.Column(db.String(256), nullable=False)
    amount = db.Column(db.Integer)
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)
    subscription_canceled = db.Column(db.Boolean, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"customer ('{self.user_id}' . '{self.status}')"
    

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    liked_user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    liked_article = db.Column(db.Integer, db.ForeignKey('article.id', ondelete='CASCADE'), nullable=False)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    image = db.Column(db.String(50), nullable=True, default='default.png')
    likes = db.relationship('Like', backref='article', passive_deletes=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"Article ('{self.title}' for the user '{self.user_id}')"