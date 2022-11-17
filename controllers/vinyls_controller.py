from flask import Blueprint, request
from init import db
from models.vinyl import Vinyl, VinylSchema
from models.comment import Comment, CommentSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


vinyls_bp = Blueprint('vinyls', __name__, url_prefix='/vinyls')

# Add a vinyl
@vinyls_bp.route('/', methods=['POST'])
@jwt_required()
def create_vinyl():
        # Create a new Vinyl model instance
        data = VinylSchema().load(request.json)
        
        vinyl = Vinyl(
            title = data['title'],
            description = data['description'],
            date = date.today(),
            status = data['status'],
            priority = data['priority'],
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


@vinyls_bp.route('/<int:id>')
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
    if vinyl:
        vinyl.title = request.json.get('title') or vinyl.title
        vinyl.description = request.json.get('description') or vinyl.description
        vinyl.status = request.json.get('status') or vinyl.status
        vinyl.priority = request.json.get('priority') or vinyl.priority
        db.session.commit()
        return VinylSchema().dump(vinyl)
    else:
        return {'error': f'Vinyl not found with id {id}'}, 404

# remove a vinyl (requires authentication)
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

@vinyls_bp.route('/<int:vinyl_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(vinyl_id):
    stmt = db.select(Vinyl).filter_by(id=vinyl_id)
    vinyl = db.session.scalar(stmt)
    if vinyl:
        comment = Comment(
            message = request.json['message'],
            user_id = get_jwt_identity(),
            vinyl = vinyl,
            date = date.today()
        )
        # Add and commit vinyl to DB
        db.session.add(comment)
        db.session.commit()
        # Respond to client
        return CommentSchema( ).dump(comment), 201
    else:
        return {'error': f'Vinyl not found with id {id}'}, 404
