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
    vinyls = db.relationship('Vinyl', back_populates='user', cascade='all, delete')

# Marshmallow schema
class UserSchema(ma.Schema):
    # Validation
    first_name = fields.String(required=True, validate=
        Regexp('^(?=\S{1,}$)[a-zA-Z ]+$', error="First name must be at least 1 letter long and contain only letters")) 

    last_name = fields.String(validate= 
        Regexp('^[a-zA-Z ]+$', error="Last name must be at least 1 letter long and contain only letters"))

    email = fields.String(required=True, validate= 
        Regexp('^[A-Za-z0-9._+\-\']+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$', error="This is not a valid email address"))
    
    password = fields.String(required=True, validate=And(
    Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^A-Za-z0-9]).{8,}$', error='Password must have at least 1 upper case, at least 1 lower case, at least 1 number, and at least 1 special character and be at least 8 characters long')
        )
    )
    class Meta:
        fields = ('id', 'first_name', 'email', 'password', 'is_admin')
        ordered = True