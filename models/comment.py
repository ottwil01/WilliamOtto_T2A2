from init import db, ma
from marshmallow import fields

# SQLAlchemy model
class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.Date)
    # Foreign keys
    comment_author = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vinyl_post_id = db.Column(db.Integer, db.ForeignKey('vinyls.id'), nullable=False)
    # Foreign key relationships
    user = db.relationship('User', back_populates='comments')
    vinyl = db.relationship('Vinyl', back_populates='comments')

# Marshmallow schema
class CommentSchema(ma.Schema):
    # Nesting attributes from imported tables
    user = fields.Nested('UserSchema', only=['id', 'name'])
    vinyl = fields.Nested('VinylSchema', only=['id', 'artist', 'album'])
    # Validation

    class Meta:
        fields = ('id', 'message', 'date', 'vinyl', 'user')
        ordered = True
