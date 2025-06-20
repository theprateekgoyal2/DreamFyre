import sys
from create_app import app
sys.path.insert(0, '/')
from app_configuration import configure_current_application


configure_current_application()


@app.route('/')
def hello():
    return '<h1>Hello World!</h1><br><i>Server is running</i>'


if __name__ == '__main__':
    app.run(debug=True)
