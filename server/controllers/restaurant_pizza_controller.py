from flask import Blueprint, jsonify, request
from server.models.restaurant_pizza import RestaurantPizza
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.config import db
from sqlalchemy.exc import IntegrityError # For handling foreign key constraints

# Create a Blueprint for restaurant_pizza routes
restaurant_pizza_bp = Blueprint('restaurant_pizza_bp', __name__, url_prefix='/restaurant_pizzas')

# POST /restaurant_pizzas
@restaurant_pizza_bp.route('/', methods=['POST'])
def create_restaurant_pizza():
    """
    Creates a new RestaurantPizza association.
    Expects JSON body with 'price', 'pizza_id', and 'restaurant_id'.
    Includes validation for price (1-30) and foreign key existence.
    Returns 201 Created on success or 400 Bad Request on error.
    """
    data = request.get_json()

    # Extract required fields from the request body
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    # Basic validation for presence of required fields
    if not all([price is not None, pizza_id is not None, restaurant_id is not None]):
        return jsonify({"errors": ["Missing required fields: 'price', 'pizza_id', 'restaurant_id'"]}), 400

    try:
        new_rp = RestaurantPizza(
            price=price,
            pizza_id=pizza_id,
            restaurant_id=restaurant_id
        )

        # Adds to session and commit to save to database
        db.session.add(new_rp)
        db.session.commit()

        # Fetch the newly created RestaurantPizza with its associated Restaurant and Pizza
        created_rp = RestaurantPizza.query.get(new_rp.id)
        if created_rp:
            response_data = created_rp.to_dict()
            response_data['pizza'] = created_rp.pizza.to_dict()
            response_data['restaurant'] = created_rp.restaurant.to_dict()
            return jsonify(response_data), 201 # 201 Created status
        else:
            # This case should ideally not happen if db.session.commit() was successful but serves as a fallback for unexpected issues.
            return jsonify({"error": "Failed to retrieve created RestaurantPizza details"}), 500

    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except IntegrityError:
        # Handles cases where pizza_id or restaurant_id do not exist in their respective tables
        db.session.rollback()
        return jsonify({"errors": ["Pizza or Restaurant not found or invalid foreign key provided."]}), 400
    except Exception as e:
        # Catch any other unexpected errors during the process
        db.session.rollback()
        return jsonify({"errors": [f"An unexpected server error occurred: {str(e)}"]}), 500

