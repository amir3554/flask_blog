from blog import db
from sqlalchemy.sql import func


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    liked_user = db.Column(db.Integer, db.ForeignKey('user.id', on_delete='CASCADE'), nullable=False)
    article_user = db.Column(db.Integer, db.ForeignKey('article.id', on_delete='CASCADE'), nullable=False)
    first_name = db.Column(db.String(30), nullable=False, unique=False)



