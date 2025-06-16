from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


mail = Mail()
bcrypt = Bcrypt()
jwt_manager = JWTManager()
