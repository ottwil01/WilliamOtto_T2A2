from init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    date = db.Column(db.Date)
    status = db.Column(db.String)
    priority = db.Column(db.String)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'), nullable=False)
    
    user = db.relationship('User', back_populates='comments')
    record = db.relationship('Record', back_populates='comments')
    
    
class CommentSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    record = fields.Nested('RecordSchema')
    
    class Meta:
        fields = ('id', 'message', 'date', 'record', 'user')
        ordered = True
 