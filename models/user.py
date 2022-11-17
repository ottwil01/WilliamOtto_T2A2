from init import db, ma
from marshmallow import fields

# SQLAlchemy model
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    # Foreign key relationships
    comments = db.relationship('Comment', back_populates='user', cascade='all, delete')
    likes = db.relationship('Like', back_populates='user', cascade='all, delete')


# Marshmallow schema
class UserSchema(ma.Schema):
    # Validation

    class Meta:
        fields = ('id', 'first_name', 'email', 'password', 'is_admin')
        ordered = True