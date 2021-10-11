from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Flask application configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf44d8000ecb0f94f01dcc7451318648'  # TODO: Add to .secrets dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/site.db'
db = SQLAlchemy(app)  # SQLAlchemy database instance created

# Password encryption
bcrypt = Bcrypt()

# Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# function name of the route we want to send the user to if they try to access a loi

# Needs to be imported after app variable is initialised to avoid circular import as routes uses app object
from flaskblog import routes
