from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Flask application configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf44d8000ecb0f94f01dcc7451318648'  # TODO: Add to .secrets dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/site.db'
db = SQLAlchemy(app)  # SQLAlchemy database instance created

# Password encryption
bcrypt = Bcrypt()

# Needs to be imported after app variable is initialised to avoid circular import as routes uses app object
from flaskblog import routes
