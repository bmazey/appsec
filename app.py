import os
import sys
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

sys.path.append(os.path.dirname(__name__))

# flask setup
app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)

# database
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run()
