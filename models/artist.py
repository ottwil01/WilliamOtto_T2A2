from init import db, ma
from marshmallow import fields

# SQLAlchemy model
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    album = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    # Foreign key relationships
    vinyl = db.relationship('Vinyl', back_populates='artists', cascade='all, delete')

# Marshmallow schema
class ArtistSchema(ma.Schema):
    # Nesting attributes from imported tables
    
    # Validation

    class Meta:
        fields = ('artist', 'album', 'genre')
        ordered = True
