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


# get one artist
@artists_bp.route('/<int:id>', methods=['GET'])
def get_one_artist(id):
    stmt = db.select(Artist).filter_by(id=id)
    artist = db.session.scalar(stmt)
    if artist:
        return ArtistSchema().dump(artist)
    else:
        return {'error': f'Artist not found with id {id}'}, 404

# update an artist (authentication required)
@artists_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_artist(id):
    stmt = db.select(Artist).filter_by(id=id)
    vinyl = db.session.scalar(stmt)
    
    return ArtistSchema().dump(artist)


# remove an artist (authentication required)
@artists_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_artist(id):
    authorize()
     
    stmt = db.select(Artist).filter_by(id=id)
    artist = db.session.scalar(stmt)
    if artist:
        db.session.delete(artist)
        db.session.commit()
        return {'message' : f" Artist '{artist.artist}' deleted successfully"}
    else:
        return {'error': f'Artist not found with id {id}'}, 404

