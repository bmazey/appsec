import os
import sys
from flask import Flask
from flask_cors import CORS
from database import db
from security import configure_authentication
from config import Config
from routes import pages
from models import User

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

    # register admin user automatically
    try:
        admin_phone = open("/run/secrets/admin_phone", "r").read().strip()
        admin_password = open("/run/secrets/admin_password", "r").read().strip()
        admin = User(username='admin', phone=admin_phone)
        admin.set_password(admin_phone, admin_password)
        db.session.add(admin)
        db.session.commit()

    except Exception:
        pass

    return app


if __name__ == '__main__':
    app = create_app()
    # init_database(app)
    # the below makes Travis mad :(
    # app.run(host='0.0.0.0')
    app.run()
