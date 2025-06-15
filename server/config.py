from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
import os

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

#initialize SQLALchemy and metadata
db = SQLAlchemy(metadata=metadata)
migrate = Migrate() 

def create_app():
     app = Flask(__name__)
    # Configure the database URI
    # Using sqlite for simplicity
     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///pizza_restaurant.db')
     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
     app.json_encoder.compact = False # For pretty printing JSON responses

    # Initialize Flask extensions
     db.init_app(app)
     migrate.init_app(app, db)

     return app