# cli.py
from app import create_app
from models import db
from flask.cli import with_appcontext

@with_appcontext
def init_db():
    db.create_all()
    print('Initialized the database.')