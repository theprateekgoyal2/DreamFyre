from flask_mail import Message
from datetime import timedelta, datetime
from extensions import mail
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token


def send_email_to_user(email, message):
    recipients = [email]

    # Creating the message
    msg = Message("Hello there!", sender="djangoprojekts@gmail.com", recipients=recipients)
    msg.body = message
    mail.send(msg)


def generate_user_tokens(user_id: int):

    access_token_expires = timedelta(minutes=30)  # Shorter expiry
    refresh_token_expires = timedelta(days=1)  # Longer expiry
    access_token = create_access_token(identity=user_id, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(identity=user_id, expires_delta=refresh_token_expires)

    return {'access_token': access_token, 'refresh_token': refresh_token}


def check_token_validity(token: str):
    try:
        data = decode_token(token)

        # Calculate expiry based on header's 'exp' claim if present
        token_expiry = datetime.utcfromtimestamp(data['exp'])
        remaining_time = token_expiry - datetime.utcnow()

        # If remaining time is sufficient (e.g., 1 minute buffer), reuse token
        buffer_time = timedelta(minutes=1)  # Adjust buffer time as needed
        if remaining_time > buffer_time:
            return {
                'message': 'Valid token, using existing one',
                'tokens': {
                    'access_token': token,
                }
            }

    except:
        return {}
