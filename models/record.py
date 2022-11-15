from init import db, ma
from marshmallow import fields

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='records')
    comments = db.relationship('Comment', back_populates='record', cascade='all, delete')
    
class RecordSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    comments = fields.List(fields.Nested('CommentSchema', exclude=['record']))
     
    class Meta:
        fields = ('id', 'title', 'description', 'status', 'priority', 'date', 'user', 'comments')
        ordered = True
 