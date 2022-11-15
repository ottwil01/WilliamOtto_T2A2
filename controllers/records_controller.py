from flask import Blueprint, request
from init import db
from models.record import Record, RecordSchema
from controllers.auth_controller import authorize
from datetime import date
from flask_jwt_extended import jwt_required


records_bp = Blueprint('records', __name__, url_prefix='/records')


@records_bp.route('/', methods=['POST'])
@jwt_required()
def create_record():
        # Create a new Record model instance
        record = Record(
            title = request.json['title'],
            description = request.json['description'],
            date = date.today(),
            status = request.json['status'],
            priority = request.json['priority']
        )
        # Add and commit record to DB
        db.session.add(record)
        db.session.commit()
        # Respond to client
        return RecordSchema( ).dump(record), 201


@records_bp.route('/')
def get_all_records():
    
    stmt = db.select(Record).order_by(Record.date.desc())
    records = db.session.scalars(stmt)
    return RecordSchema(many=True).dump(records)


@records_bp.route('/<int:id>')
def get_one_record(id):
    stmt = db.select(Record).filter_by(id=id)
    record = db.session.scalar(stmt)
    if record:
        return RecordSchema().dump(record)
    else:
        return {'error': f'Record not found with id {id}'}, 404


@records_bp.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_one_record(id):
    stmt = db.select(Record).filter_by(id=id)
    record = db.session.scalar(stmt)
    if record:
        record.title = request.json.get('title') or record.title
        record.description = request.json.get('description') or record.description
        record.status = request.json.get('status') or record.status
        record.priority = request.json.get('priority') or record.priority
        db.session.commit()
        return RecordSchema().dump(record)
    else:
        return {'error': f'Record not found with id {id}'}, 404


@records_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_one_record(id):
    authorize()
     
    stmt = db.select(Record).filter_by(id=id)
    record = db.session.scalar(stmt)
    if record:
        db.session.delete(record)
        db.session.commit()
        return {'message' : f" Record '{record.title}' deleted successfully"}
    else:
        return {'error': f'Record not found with id {id}'}, 404