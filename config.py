# config.py

import os
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False


SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-secret-and-hard-to-guess-string'