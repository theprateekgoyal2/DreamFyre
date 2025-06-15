from .apis import register_user_api, login_user_api


api_routes = [
    ('/user/register', register_user_api, ['POST']),
    ('/user/login', login_user_api, ['POST'])
]
