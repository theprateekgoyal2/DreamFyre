import os
import sqlite3
from dotenv import load_dotenv
from sqlalchemy.dialects import sqlite

basedir = os.path.abspath(os.path.dirname(__file__))

SQL_INSTANCE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
