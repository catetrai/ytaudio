from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create application
app = Flask(__name__)

# Set configs from Config class
app.config.from_object(Config)

### Begin Flask extensions
# DB instance
db = SQLAlchemy(app)

# DB migration engine
migrate = Migrate(app, db)

from app import routes, models, errors, filters
