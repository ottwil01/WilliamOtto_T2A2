from flask import Blueprint, request
from init import db
from models.vinyl import Vinyl, VinylSchema
from models.comment import Comment, CommentSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


# Likes Controller Blueprint
likes_bp = Blueprint('likes', __name__, url_prefix='/likes')

# Make a like
@likes_bp.route('/<int:vinyl_id>/likes', methods=['POST'])
@jwt_required()
def create_like(vinyl_id):
    stmt = db.select(Vinyl).filter_by(id=vinyl_id)
    vinyl = db.session.scalar(stmt)
    if vinyl:
        like = Like(
            user_id = get_jwt_identity(),
            vinyl = vinyl,
            date = date.today()
        )
        # Add and commit vinyl to DB
        db.session.add(like)
        db.session.commit()
        # Respond to client
        return LikeSchema().dump(like), 201
    else:
        return {'error': f'Vinyl not found with id {id}'}, 404

# Delete a like
@likes_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_like(id):

    # Query to find like by ID
    stmt = db.select(Like).filter_by(id=id)
    like = db.session.scalar(stmt)
    
    # If found
    if like:

        # Like deleted and change committed to database
        db.session.delete(like)
        db.session.commit()

        # Respond to client
        return {'message': f"Like No.{like.id} removed successfully"}
    
    # If not found
    else:
        return {'error': f'No like with id {id}'}, 404