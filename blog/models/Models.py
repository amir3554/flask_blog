from blog import db
from sqlalchemy.sql import func

    

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