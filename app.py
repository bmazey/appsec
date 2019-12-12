import os
import sys
from flask import Flask
from flask_cors import CORS
from database import db
from security import configure_authentication
from config import Config
from routes import pages

sys.path.append(os.path.dirname(__name__))


# flask setup
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    configure_authentication(app)

    # routing blueprint
    app.register_blueprint(pages)

    CORS(app)

    return app


if __name__ == '__main__':
    app = create_app()
    # init_database(app)
    # the below makes Travis mad :(
    # app.run(host='0.0.0.0')
    app.run()
