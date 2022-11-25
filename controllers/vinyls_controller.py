from flask import Blueprint, request
from init import db
from models.vinyl import Vinyl, VinylSchema
from models.comment import Comment, CommentSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


# Vinyls Controller Blueprint
vinyls_bp = Blueprint('vinyls', __name__, url_prefix='/vinyls')


# Get all vinyl by artist
@vinyls_bp.route('/artist/<int:id>/', methods=['GET'])
@jwt_required()
def artist_vinyls(artist_id):
    
    # Query to find vinyl by artist ID
    stmt = db.select(Artist).filter_by(artist_id=artist_id)
    vinyl = db.session.scalars(stmt)

    # Respond to client with all vinyls by artist excluding linked comments, likes and artist
    return ArtistSchema(many=True, exclude=['id', 'comments', 'likes']).dump(vinyl)

# Add a vinyl
@vinyls_bp.route('/', methods=['POST'])
@jwt_required()
def create_vinyl():
        # Create a new Vinyl model instance
        data = VinylSchema().load(request.json)
        
        vinyl = Vinyl(
            artist_id = data['artist_id'],
            date = date.today(),
            user_id = get_jwt_identity()
        )
        # Add and commit vinyl to DB
        db.session.add(vinyl)
        db.session.commit()
        # Respond to client
        return VinylSchema().dump(vinyl), 201


# get all vinyls
@vinyls_bp.route('/')
def get_all_vinyls():
    
    stmt = db.select(Vinyl).order_by(Vinyl.date.desc())
    vinyls = db.session.scalars(stmt)
    return VinylSchema(many=True).dump(vinyls)

# get one vinyl
@vinyls_bp.route('/<int:id>', methods=['GET'])
def get_one_vinyl(id):
    stmt = db.select(Vinyl).filter_by(id=id)
    vinyl = db.session.scalar(stmt)
    if vinyl:
        return VinylSchema().dump(vinyl)
    else:
        return {'error': f'Vinyl not found with id {id}'}, 404

# update a vinyl (authentication required)
@vinyls_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_vinyl(id):
    stmt = db.select(Vinyl).filter_by(id=id)
    vinyl = db.session.scalar(stmt)
    
    return VinylSchema().dump(vinyl)


# remove a vinyl (authentication required)
@vinyls_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_vinyl(id):
    authorize()
     
    stmt = db.select(Vinyl).filter_by(id=id)
    vinyl = db.session.scalar(stmt)
    if vinyl:
        db.session.delete(vinyl)
        db.session.commit()
        return {'message' : f" Vinyl '{vinyl.title}' deleted successfully"}
    else:
        return {'error': f'Vinyl not found with id {id}'}, 404

