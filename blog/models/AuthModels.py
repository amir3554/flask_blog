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
    subscription_type = db.Column(db.String(256))
    status = db.Column(db.String(32), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="RESTRICT"))
    customer_id = db.Column(db.String(256), nullable=True)
    subscription_id = db.Column(db.String(256))
    amount = db.Column(db.Integer, nullable=True)
    subscription_start = db.Column(db.DateTime, nullable=True)
    subscription_end = db.Column(db.DateTime, nullable=True)
    subscription_canceled = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self) -> str:
        return f"customer ('{self.user_id}' . '{self.status}')"