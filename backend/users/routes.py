from .apis import register_user_api, login_user_api


api_routes = [
    ('/api/user/register', register_user_api, ['POST']),
    ('/api/user/login', login_user_api, ['POST'])
]
