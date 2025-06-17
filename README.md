# Pizza Restaurant API
This project implements a RESTful API for a Pizza Restaurant using Flask, following the MVC (Model-View-Controller) architectural pattern. It allows managing restaurants, pizzas, and their associations.

# Project Structure
.
├── server/
│   ├── __init__.py         # Package initialization
│   ├── app.py              # Main Flask application setup and route registration
│   ├── config.py           # Database configuration and Flask-SQLAlchemy setup
│   ├── models/             # Database Models (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── restaurant.py
│   │   ├── pizza.py
│   │   └── restaurant_pizza.py
│   ├── controllers/        # Route Handlers (Controllers)
│   │   ├── __init__.py
│   │   ├── restaurant_controller.py
│   │   ├── pizza_controller.py
│   │   └── restaurant_pizza_controller.py
│   └── seed.py             # Script to seed the database with initial data
├── migrations/             # Flask-Migrate directory for database migrations
├── challenge-1-pizzas.postman_collection.json # Postman collection for testing
└── README.md               # This README file


# Setup Instructions
Follow these steps to set up and run the API locally:

1. Create a Virtual Environment and Install Dependencies
Navigate to the root directory of the project in your terminal.

## Create a pipenv virtual environment and install packages
pipenv install flask flask_sqlalchemy flask_migrate flask_cors
## Activate the virtual environment
pipenv shell


2. Database Setup and Migration
Set the FLASK_APP and PYTHONPATH environment variables to point to your main application file and project root, respectively.

export PYTHONPATH=$(pwd)
export FLASK_APP=server/app.py


Initialize, migrate, and upgrade your database. This creates the database file (pizza_restaurant.db) and sets up the tables based on your models.

## Initialize Flask-Migrate for the project
flask db init
## Create a migration script based on your models
flask db migrate -m "Initial migration"
## Apply the migrations to your database
flask db upgrade

3. Seed the Database
Populate your database with some initial data using the seed.py script:

python server/seed.py

4. Run the Flask Application
flask run

The API should now be running on http://127.0.0.1:5000/ (or http://localhost:5000/).

# Models
The application uses the following SQLAlchemy models:

## Restaurant
id: Primary Key
name: String, not nullable
address: String, not nullable
Relationships: Has many RestaurantPizzas. Cascading deletes are configured so that deleting a Restaurant also deletes all associated RestaurantPizza entries.

## Pizza
id: Primary Key
name: String, not nullable
ingredients: String, not nullable
Relationships: Has many RestaurantPizzas.

## RestaurantPizza (Join Table)
id: Primary Key
price: Integer, not nullable.
Validation: Must be between 1 and 30 (inclusive).
restaurant_id: Foreign Key referencing restaurants.id
pizza_id: Foreign Key referencing pizzas.id
Relationships: Belongs to Restaurant and Pizza.

# Required Routes
All routes return JSON responses. Errors are returned with appropriate HTTP status codes and a JSON error object.

1. GET /restaurants
Description: Returns a list of all restaurants.

Method: GET

URL: /restaurants

Example Request:

GET /restaurants HTTP/1.1
Host: localhost:5000


Example Success Response (Status: 200 OK):

[
    {
        "address": "123 Main St",
        "id": 1,
        "name": "Sausage Pizza"
    },
    {
        "address": "456 Oak Ave",
        "id": 2,
        "name": "Pepperoni Pizza"
    },
    {
        "address": "789 Pine Ln",
        "id": 3,
        "name": "Kiki's Pizza"
    }
]


2. GET /restaurants/<int:id>
Description: Returns details of a single restaurant, including its associated pizzas and their prices.

Method: GET

URL: /restaurants/<int:id>

Example Request:

GET /restaurants/1 HTTP/1.1
Host: localhost:5000


Example Success Response (Status: 200 OK):

{
    "address": "123 Main St",
    "id": 1,
    "name": "Sausage Pizza",
    "pizzas": [
        {
            "id": 1,
            "ingredients": "Dough, Tomato Sauce, Mozzarella, Oregano",
            "name": "Cheese",
            "price": 10
        },
        {
            "id": 2,
            "ingredients": "Dough, Tomato Sauce, Mozzarella, Pepperoni",
            "name": "Pepperoni",
            "price": 12
        }
    ]
}


Example Error Response (Status: 404 Not Found):

{
    "error": "Restaurant not found"
}


3. DELETE /restaurants/<int:id>
Description: Deletes a restaurant and all related RestaurantPizzas entries.

Method: DELETE

URL: /restaurants/<int:id>

Example Request:

DELETE /restaurants/1 HTTP/1.1
Host: localhost:5000


Example Success Response (Status: 204 No Content):
(No content is returned in the response body)

Example Error Response (Status: 404 Not Found):

{
    "error": "Restaurant not found"
}


4. GET /pizzas
Description: Returns a list of all pizzas.

Method: GET

URL: /pizzas

Example Request:

GET /pizzas HTTP/1.1
Host: localhost:5000


Example Success Response (Status: 200 OK):

[
    {
        "id": 1,
        "ingredients": "Dough, Tomato Sauce, Mozzarella, Oregano",
        "name": "Cheese"
    },
    {
        "id": 2,
        "ingredients": "Dough, Tomato Sauce, Mozzarella, Pepperoni",
        "name": "Pepperoni"
    },
    {
        "id": 3,
        "ingredients": "Dough, Tomato Sauce, Mozzarella, Mushrooms, Olives, Bell Peppers",
        "name": "Vegetable"
    }
]


5. POST /restaurant_pizzas
Description: Creates a new RestaurantPizza association. Includes validation for the price.

Method: POST

URL: /restaurant_pizzas

Request Body (JSON):

{
    "price": 5,
    "pizza_id": 1,
    "restaurant_id": 3
}


Example Success Response (Status: 201 Created):

{
    "id": 7,
    "pizza": {
        "id": 1,
        "ingredients": "Dough, Tomato Sauce, Mozzarella, Oregano",
        "name": "Cheese"
    },
    "pizza_id": 1,
    "price": 5,
    "restaurant": {
        "address": "789 Pine Ln",
        "id": 3,
        "name": "Kiki's Pizza"
    },
    "restaurant_id": 3
}


Example Error Response (Status: 400 Bad Request) - Price Validation:

{
    "errors": [
        "Price must be between 1 and 30"
    ]
}


Example Error Response (Status: 400 Bad Request) - Missing Fields:

{
    "errors": [
        "Missing required fields: 'price', 'pizza_id', 'restaurant_id'"
    ]
}


Example Error Response (Status: 400 Bad Request) - Invalid Foreign Key:

{
    "errors": [
        "Pizza or Restaurant not found or invalid foreign key provided."
    ]
}
