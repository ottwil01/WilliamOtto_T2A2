from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

# SQLAlchemy model
class Vinyl(db.Model):
    __tablename__ = 'vinyls'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artist_id = db.Column(db.String, db.ForeignKey('artists.artist'), nullable=False)
    # Foreign key relationships
    artist = db.relationship('Artist', back_populates='vinyls')
    user = db.relationship('User', back_populates='vinyls')
    comments = db.relationship('Comment', back_populates='vinyl', cascade='all, delete')
    likes = db.relationship('Like', back_populates='vinyl', cascade='all, delete')

# Marshmallow schema
class VinylSchema(ma.Schema):
    # Nesting attributes from imported tables
    artist = fields.Nested('ArtistSchema', only=['name', 'album', 'genre'])
    user = fields.Nested('UserSchema', only=['name'])
    comments = fields.List(fields.Nested('CommentSchema', only=['user', 'message', 'date']))
    likes = fields.List(fields.Nested('LikeSchema', only=['like_author', 'date']))

    class Meta:
        fields = ('id', 'artist', 'user', 'comments', 'likes', 'date')
        ordered = True
 