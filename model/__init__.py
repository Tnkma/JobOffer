import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
Base = db.Model

bcrypt = Bcrypt(app)

# initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'plum.login'
login_manager.login_message_category = 'info'

# initialize the login manager
login_manager = LoginManager(app)
login_manager.login_view = 'client_s.login'
login_manager.login_message_category = 'info'

from model.plumbers.routes import plums
from model.clients.routes import client_s
from model.jobs.routes import job_route
from model.main.routes import main

app.register_blueprint(plums)
app.register_blueprint(client_s)
app.register_blueprint(job_route)
app.register_blueprint(main)
