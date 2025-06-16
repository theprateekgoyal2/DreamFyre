import os
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SQL_INSTANCE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
