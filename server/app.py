from server.config import create_app, db
from flask import Flask, jsonify
from flask_cors import CORS # Import CORS for cross-origin resource sharing

# Import your models here so Flask-Migrate can detect them
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.models.restaurant_pizza import RestaurantPizza

# Create the Flask application instance
app = create_app()
CORS(app) # Enable CORS for all routes

# Define a simple root route for testing if the app is running
@app.route('/')
def home():
    return '<h1>Pizza Restaurant API</h1><p>Welcome to the Pizza Restaurant API!</p>'

# This block allows you to run the app directly using `python app.py`
# It's mainly for local development and testing.
if __name__ == '__main__':
    # Ensure the database tables are created if running directly
    # Note: For production, you'd typically rely on `flask db upgrade`
    with app.app_context():
        db.create_all() # This creates tables based on models if they don't exist
    app.run(port=5555, debug=True)


