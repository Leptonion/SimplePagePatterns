from flask import Flask
from .db_patterns import DBConnector

cursor = DBConnector()
cursor.create_db_file()


def create_app():
    app = Flask(__name__, static_folder='static')

    app.config['SECRET_KEY'] = 'Arm0rArt'

    from .main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
