from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os

# Define metadata naming convention for SQLAlchemy
# This helps with consistent naming of constraints and indexes, which is good practice.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

# Initialize SQLAlchemy with the metadata
db = SQLAlchemy(metadata=metadata)
migrate = Migrate() # Initialize Migrate without app here, will initialize with app later

def create_app():
    app = Flask(__name__)
    # Configure the database URI
    # Using sqlite for simplicity, stored in the current directory
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///pizza_restaurant.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.json_encoder.compact = False # OLD: For pretty printing JSON responses - REMOVE OR COMMENT OUT THIS LINE
    # NEW: For pretty printing JSON responses in debug mode or if explicitly needed
    app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    return app
