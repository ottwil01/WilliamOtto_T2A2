from flask import Blueprint
from init import db, bc
from models.record import Record
from models.user import User
from datetime import date
from models.comment import Comment
 

db_commands = Blueprint('db', __name__ )
 

# Define a custom CLI (terminal) command
@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bc.generate_password_hash('eggs').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='someone@spam.com',
            password=bc.generate_password_hash('12345').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    records = [
        Record(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today(),
            user = users[0]
        ),
        Record(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today(),
            user = users[0]
        ),
        Record(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today(),
            user = users[1]
        ),
        Record(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today(),
            user = users[1]
        )
    ]

    db.session.add_all(records)
    db.session.commit()
    
    comments = [
        Comment(
            message = 'comment 1',
            user = users[0],
            record = records[0],
            date = date.today()
        ),
        Comment(
            message = 'comment 2',
            user = users[1],
            record = records[2],
            date = date.today()
        ),
        Comment (
            message = 'comment 3',
            user = users[1],
            record = records[3],
            date = date.today()
        )
    ]
    
    db.session.add_all(comments)
    db.session.commit()
    
    print('Tables seeded')
