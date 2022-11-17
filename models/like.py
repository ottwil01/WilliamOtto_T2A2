from init import db, ma
from marshmallow import fields

# SQLAlchemy model
class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    # Foreign keys
    vinyl_post_id = db.Column(db.String, db.ForeignKey('vinyl.id'), nullable=False)
    like_author = db.Column(db.String, db.ForeignKey('user.name'), nullable=False)
    # Foreign key relationships

# Marshmallow schema
class LikeSchema(ma.Schema):
    # Nesting attributes from imported tables

    # Validation

    class Meta:
        fields = ('like_author')
        ordered = True
