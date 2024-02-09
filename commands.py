from main import db
from flask import Blueprint
from main import bcrypt
from models.users import User
from models.cards import Card
from models.comments import Comment
from datetime import date

db_commands = Blueprint("db", __name__)

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@db_commands .cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands .cli.command("seed")
def seed_db():

    #Create the users first
    admin_user = User(
        email = "admin@email.com",
        password = bcrypt.generate_password_hash("password123").decode("utf-8"),
        admin = True
    )
    db.session.add(admin_user)

    user1 = User(
        email = "user1@email.com",
        password = bcrypt.generate_password_hash("123456").decode("utf-8")
    )
    db.session.add(user1)
    # This extra commit will end the transaction and generate the ids for the user
    db.session.commit()

    # create the card object
    card1 = Card(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        title = "Start the project",
        description = "Stage 1, creating the database",
        status = "To Do",
        priority = "High",
        date = date.today(),
        user_id = user1.id
    )
    # Add the object as a new row to the table
    db.session.add(card1)

    card2 = Card(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        title = "SQLAlchemy and Marshmallow",
        description = "Stage 2, integrate both modules in the project",
        status = "Ongoing",
        priority = "High",
        date = date.today(),
        # it also can be done this way
        user = user1
    )
    # Add the object as a new row to the tablef
    db.session.add(card2)

    # commit the changes to have card id ready
    db.session.commit()

    comment1 = Comment(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        message = "Created the database and users in PostgreSQL ",
        user = user1,
        card = card1
    )
    # Add the object as a new row to the table
    db.session.add(comment1)

    comment2 = Comment(
        message = "Make sure you check the database authentication",
        user = admin_user,
        card = card1
    )
    # Add the object as a new row to the table
    db.session.add(comment2)

    comment3 = Comment(
        message = "Go to the official documentation when errors",
        user = user1,
        card = card2
    )
    # Add the object as a new row to the table
    db.session.add(comment3)

    # commit the changes
    db.session.commit()


    print("Table seeded") 

@db_commands .cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")  