import os
from dotenv import load_dotenv
from extensions import mail, bcrypt, jwt_manager
from flask import Flask


load_dotenv()


def create_app():
    app = Flask(__name__)

    # Set debug mode explicitly
    app.config['DEBUG'] = True
    app.config['ENV'] = 'development'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # SMTP Credentials
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mail.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)

    return app
