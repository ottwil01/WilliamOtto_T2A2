from init import db, ma
from marshmallow import fields

# SQLAlchemy model
class Like(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)

    # Foreign keys
    vinyl_post_id = db.Column(db.String, db.ForeignKey('vinyls.id'), nullable=False)
    like_author = db.Column(db.String, db.ForeignKey('users.id'), nullable=False)
    # Foreign key relationships
    user = db.relationship('User', back_populates='comments')
    vinyl = db.relationship('Vinyl', back_populates='comments')
    
# Marshmallow schema
class LikeSchema(ma.Schema):
    # Nesting attributes from imported tables
    user = fields.Nested('UserSchema', only=['id', 'name'])
    vinyl = fields.Nested('VinylSchema', only=['id', 'artist', 'album'])

    # Validation

    class Meta:
        fields = ('like_artist')
        ordered = True
