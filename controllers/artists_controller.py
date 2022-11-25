from flask import Blueprint, request
from init import db
from models.vinyl import Vinyl, VinylSchema
from models.comment import Comment, CommentSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity

# Artists Controller Blueprint
artists_bp = Blueprint('artists', __name__, url_prefix='/artists')

@artists_bp.route('/', methods=['GET'])
@jwt_required()
def all_artists():

    # Query to get all artists
    stmt = db.select(Artist)
    artists = db.session.scalars(stmt)
    
    # Respond to client with all artists
    return ArtistSchema(many=True).dump(artists)


# Get one artist by ID (requires authentication)
@artists_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def one_artist(id):
    
    # Query to find artist by ID
    stmt = db.select(Artist).filter_by(id=id)
    artist = db.session.scalar(stmt)
    
    # If found
    if artist:
        
        # Respond to client with artist
        return ArtistSchema().dump(artist)
    
    # If not found
    else:
        return {'error': f'No artist with id {id}'}, 404
    
    # Get one artist by ID (requires authentication)
@artists_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def one_artist(id):
    
    # Query to find artist by ID
    stmt = db.select(Artist).filter_by(id=id)
    artist = db.session.scalar(stmt)
    
    # If found
    if artist:
        
        # Respond to client with artist
        return ArtistSchema().dump(artist)
    
    # If not found
    else:
        return {'error': f'No artist with id {id}'}, 404