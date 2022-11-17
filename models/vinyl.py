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

    # Validation
    # comments = fields.List(fields.Nested('CommentSchema', exclude=['vinyl']))
    # likes = fields.List(fields.Nested('LikeSchema'))
    
    # title = fields.String(required=True, validate=And(
    #     Length(min=2),
    #     Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed')
    #     )
    # )
    # status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))
    # priority = fields.String(required=True, validate=OneOf(VALID_PRIORITIES))

    # @validates('status')
    # def validate_status(self, value):
    #     # If trying to set this vinyl to 'Ongoing' ...
    #     if value == VALID_STATUSES[1]:
    #         stmt = db.select(db.func.count()).select_from(Vinyl).filter_by(status=VALID_STATUSES[1])
    #         count = db.session.scalar(stmt)
    #         # ... and there is already an ongoing vinyl in the database
    #         if count > 0:
    #             raise ValidationError('You already have an ongoing vinyl')

    class Meta:
        fields = ('id', 'artist', 'user', 'comments', 'likes', 'date')
        ordered = True
 