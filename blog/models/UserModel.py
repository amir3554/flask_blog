from blog import db
from sqlalchemy.sql import func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    join_date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    first_name = db.Column(db.String(30), nullable=False, unique=False)
    last_name = db.Column(db.String(30), nullable=False, unique=False)
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(32), nullable=False, unique=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    articles = db.relationship("Article", backref='user', lazy=True)
    stripe_customer = db.relationship("SrtipeCustomer", backref='user')
    likes = db.relationship('Like', backref='user', passive_deletes=True)

    def __repr__(self) -> str:
        return f"User ('{self.username}' . '{self.email}')"
