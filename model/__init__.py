import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.config['SECRET_KEY'] = '5421691148efa035624f86ae37a3964f6775ee7870c65c9687ee82b790f69c05'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Base = db.Model

bcrypt = Bcrypt(app)

# initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.blueprint_login_views = {
    'plums': 'plums.login',
    'client_s': 'client_s.login'
}
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'


from model.plumbers.routes import plums
from model.clients.routes import client_s
from model.jobs.routes import job_route
from model.main.routes import main
from .base import Plumber, Client


@login_manager.user_loader
def load_user(user_id):
    """ Loads the user """
    x = Plumber.query.get(str(user_id))
    if x == None:
        x = Client.query.get(str(user_id))
        
    return x


app.register_blueprint(plums)
app.register_blueprint(client_s)
app.register_blueprint(job_route)
app.register_blueprint(main)
