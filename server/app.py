from server.config import create_app, db
from flask import Flask, jsonify
from flask_cors import CORS # Import CORS for cross-origin resource sharing

# Imports the models
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.models.restaurant_pizza import RestaurantPizza

# Imports the Blueprints from your controllers
from server.controllers.restaurant_controller import restaurant_bp
from server.controllers.pizza_controller import pizza_bp
from server.controllers.restaurant_pizza_controller import restaurant_pizza_bp

app = create_app()
CORS(app) # Enable CORS for all routes

# These lines link the controllers to the Flask app
app.register_blueprint(restaurant_bp)
app.register_blueprint(pizza_bp)
app.register_blueprint(restaurant_pizza_bp)


# Defines a simple root route for testing if the app is running
@app.route('/')
def home():
    return '<h1>Pizza Restaurant API</h1><p>Welcome to the Pizza Restaurant API!</p>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)
