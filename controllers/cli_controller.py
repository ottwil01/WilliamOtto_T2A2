from flask import Blueprint
from init import db, bc
from models.vinyl import Vinyl
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
            email='will@spam.com',
            password=bc.generate_password_hash('12345').decode('utf-8'),
            is_admin=True
        ),
        User(
            email='someone1@spam.com',
            password=bc.generate_password_hash('12345').decode('utf-8')
        ),
        User(
            email='someone2@spam.com',
            password=bc.generate_password_hash('12345').decode('utf-8')
        ),
        User(
            email='someone3@spam.com',
            password=bc.generate_password_hash('12345').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    vinyls = [
        Vinyl(
            artist = "Green Day",
            genre = "Punk",
            date = date.today(),
            user = users[0]
        ),
        Vinyl(
            artist = "Led Zeppelin",
            genre = "Rock, Heavy Metal",
            date = date.today(),
            user = users[1]
        ),
        Vinyl(
            artist = "The Police",
            genre = "Rock",
            date = date.today(),
            user = users[2]
        ),
        Vinyl(
            artist = "Cat Stevens",
            genre = "Folk, Pop",
            date = date.today(),
            user = users[3]
        )
    ]

    db.session.add_all(vinyls)
    db.session.commit()
    
    comments = [
        Comment(
            message = 'comment 1',
            user = users[0],
            vinyl = vinyls[0],
            date = date.today()
        ),
        Comment(
            message = 'comment 2',
            user = users[1],
            vinyl = vinyls[2],
            date = date.today()
        ),
        Comment (
            message = 'comment 3',
            user = users[1],
            vinyl = vinyls[3],
            date = date.today()
        ),
        Comment(
            message = 'comment 4',
            user = users[2],
            vinyl = vinyls[1],
            date = date.today()
        ),
        Comment(
            message = 'comment 5',
            user = users[2],
            vinyl = vinyls[2],
            date = date.today()
        ),
        Comment (
            message = 'comment 6',
            user = users[3],
            vinyl = vinyls[3],
            date = date.today()
        )
    ]
    likes = [
        Like(
            like_author = users[1],
            vinyl = vinyls[0],
        ),
        Like(
            like_author = users[2],
            vinyl = vinyls[0],
        ),
        Like(
            like_author = users[3],
            vinyl = vinyls[0],
        ),
        Like(
            like_author = users[0],
            vinyl = vinyls[1],
        ),
        Like(
            like_author = users[1],
            vinyl = vinyls[1],
        ),
        Like(
            like_author = users[0],
            vinyl = vinyls[2],
        ),
        Like(
            like_author = users[1],
            vinyl = vinyls[2],
        ),
        Like(
            like_author = users[2],
            vinyl = vinyls[2],
        ),
        Like(
            like_author = users[3],
            vinyl = vinyls[2],
        ),
        Like(
            like_author = users[0],
            vinyl = vinyls[3],
        ),
        Like(
            like_author = users[1],
            vinyl = vinyls[3],
        ),
        Like(
            like_author = users[3],
            vinyl = vinyls[3],
        )
    ]


    db.session.add_all(comments)
    db.session.commit()
    
    print('Tables seeded')
