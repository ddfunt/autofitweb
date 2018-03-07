#from autofit_app import app, db
from autofit_app.models import User, Post
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from autofit_app import routes, models

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}