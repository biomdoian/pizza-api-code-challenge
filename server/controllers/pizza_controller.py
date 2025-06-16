from flask import Blueprint, jsonify
from server.models.pizza import Pizza

# Creates a Blueprint for pizza routes
pizza_bp = Blueprint('pizza_bp', __name__, url_prefix='/pizzas')

# GET /pizzas
@pizza_bp.route('/', methods=['GET'])
def get_pizzas():
    """
    Returns a list of all pizzas.
    """
    pizzas = Pizza.query.all()
    # Serialize pizzas to a list of dictionaries
    pizza_list = [p.to_dict() for p in pizzas]
    return jsonify(pizza_list), 200
