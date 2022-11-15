from init import db, ma
from marshmallow import fields, validates
from marshmallow.validate import Length, OneOf, And, Regexp
from marshmallow.exceptions import ValidationError

VALID_PRIORITIES = ('Urgent', 'High', 'Medium', 'Low')
VALID_STATUSES = ('To do', 'Ongoing', 'Done', 'Testing', 'Deployed')

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String, default=VALID_STATUSES[0])
    priority = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', back_populates='records')
    comments = db.relationship('Comment', back_populates='record', cascade='all, delete')

class RecordSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['record']))
    title = fields.String(required=True, validate=And(
        Length(min=2),
        Regexp('^[a-zA-Z0-9 ]+$', error='Only letters, numbers and spaces are allowed')
        )
    )
    status = fields.String(load_default=VALID_STATUSES[0], validate=OneOf(VALID_STATUSES))
    priority = fields.String(required=True, validate=OneOf(VALID_PRIORITIES))

    @validates('status')
    def validate_status(self, value):
        # If trying to set this record to 'Ongoing' ...
        if value == VALID_STATUSES[1]:
            stmt = db.select(db.func.count()).select_from(Record).filter_by(status=VALID_STATUSES[1])
            count = db.session.scalar(stmt)
            # ... and there is already an ongoing record in the database
            if count > 0:
                raise ValidationError('You already have an ongoing record')


    class Meta:
        fields = ('id', 'title', 'description', 'status', 'priority', 'date', 'user', 'comments')
        ordered = True
 