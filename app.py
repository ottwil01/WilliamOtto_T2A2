from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, timedelta
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

app.config ['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://vinyl_dev:password123@127.0.0.1:5432/vinyl'
app.config['JWT_SECRET_KEY'] = 'hello there'

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password', 'is_admin')

@app.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")
    
@app.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='someone@spam.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8')
        )
    ]

    # cards = [
    #     Card(
    #         title = 'Start the project',
    #         description = 'Stage 1 - Create the database',
    #         status = 'To Do',
    #         priority = 'High',
    #         date = date.today()
    #     ),
    #     Card(
    #         title = "SQLAlchemy",
    #         description = "Stage 2 - Integrate ORM",
    #         status = "Ongoing",
    #         priority = "High",
    #         date = date.today()
    #     ),
    #     Card(
    #         title = "ORM Queries",
    #         description = "Stage 3 - Implement several queries",
    #         status = "Ongoing",
    #         priority = "Medium",
    #         date = date.today()
    #     ),
    #     Card(
    #         title = "Marshmallow",
    #         description = "Stage 4 - Implement Marshmallow to jsonify models",
    #         status = "Ongoing",
    #         priority = "Medium",
    #         date = date.today()
    #     )
    # ]

    # db.session.add_all(cards)
    db.session.add_all(users)
    db.session.commit()
    print('Tables seeded')


@app.route('/')
def index():
    return "Hello, world!"