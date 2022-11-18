from flask import Blueprint, request
from init import db
from models.vinyl import Vinyl, VinylSchema
from models.comment import Comment, CommentSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity


# Comments Controller Blueprint
comments_bp = Blueprint('comments', __name__, url_prefix='/comments')


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


@comments_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_comment(id):

    # Query to find comment by ID
    stmt = db.select(Comment).filter_by(id=id)
    comment = db.session.scalar(stmt)
    
    # If found
    if comment:

        # Comment deleted and change committed to database
        db.session.delete(comment)
        db.session.commit()

        # Respond to client
        return {'message': f"Comment No.{comment.id} deleted successfully"}
    
    # If not found
    else:
        return {'error': f'No comment with id {id}'}, 404