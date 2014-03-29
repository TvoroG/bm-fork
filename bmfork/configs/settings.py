import os
basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# DB
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/dbname'
