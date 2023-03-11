from flask import Flask
from routes import blueprints
from utils import register_routes


app = Flask(__name__)
register_routes(app, blueprints)


def main():
    app.run(debug=True)
    return True


__name__ == '__main__' and main()