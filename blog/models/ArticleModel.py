from blog import db
from sqlalchemy.sql import func


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.Column(db.String(50), nullable=True, default='default.png')
    likes = db.relationship('Like', backref='article', passive_deletes=True)

    def __repr__(self) -> str:
        return f"Article ('{self.title}' for the user '{self.user_id}')"