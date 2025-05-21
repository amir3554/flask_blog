from blog import db
from sqlalchemy.sql import func


class StripeCustomer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    subscription_type = db.Column(db.String(256), nullable=False)
    status = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subscription_id = db.Column(db.String(256), nullable=False)
    amount = db.Column(db.Integer)
    subscription_start = db.Column(db.DateTime)
    subscription_end = db.Column(db.DateTime)
    subscription_canceled = db.Column(db.Boolean, nullable=True)

    def __repr__(self) -> str:
        return f"customer ('{self.user_id}' . '{self.status}')"