from flask import Blueprint, jsonify, make_response, request
from server.models.restaurant import Restaurant
from server.models.restaurant_pizza import RestaurantPizza
from server.config import db

# Create a Blueprint for restaurant routes
restaurant_bp = Blueprint('restaurant_bp', __name__, url_prefix='/restaurants')

# GET /restaurants
@restaurant_bp.route('/', methods=['GET'])
def get_restaurants():
    """
    Returns a list of all restaurants.
    """
    restaurants = Restaurant.query.all()
    # Serialize restaurants to a list of dictionaries
    restaurant_list = [r.to_dict() for r in restaurants]
    return jsonify(restaurant_list), 200

# GET /restaurants/<int:id>
@restaurant_bp.route('/<int:id>', methods=['GET'])
def get_restaurant_by_id(id):
    """
    Returns details of a single restaurant and its pizzas.
    Returns 404 if the restaurant is not found.
    """
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    # Serialize restaurant and its associated pizzas with prices
    restaurant_data = restaurant.to_dict()
    pizzas_data = []
    # Loop through the join table to get both pizza info and price
    for rp in restaurant.restaurant_pizzas:
        pizza_info = rp.pizza.to_dict() # Get pizza details
        pizza_info['price'] = rp.price # Add price from the join table
        pizzas_data.append(pizza_info)

    restaurant_data['pizzas'] = pizzas_data
    return jsonify(restaurant_data), 200

# DELETE /restaurants/<int:id>
@restaurant_bp.route('/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    """
    Deletes a restaurant and all related RestaurantPizzas due to cascading delete.
    Returns 204 No Content on success, 404 if not found.
    """
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404

    try:
        # Cascading delete is set up in the Restaurant model
        db.session.delete(restaurant)
        db.session.commit()
        # Return 204 No Content for successful deletion as per REST best practices
        return make_response('', 204)
    except Exception as e:
        db.session.rollback() # Rollback changes if an error occurs
        # In a real application, you might log the error 'str(e)'
        return jsonify({"error": "An error occurred during deletion"}), 500

