from server.app import app, db
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.models.restaurant_pizza import RestaurantPizza

def seed_database():
    with app.app_context():
        print("Starting database seeding...")

        # Clear existing data to ensure a fresh seed every time
        print("Clearing existing data...")
        RestaurantPizza.query.delete()
        Restaurant.query.delete()
        Pizza.query.delete()
        db.session.commit()
        print("Existing data cleared.")

        # Create sample Restaurants
        print("Creating restaurants...")
        restaurant1 = Restaurant(name="Sausage Pizza", address="123 Main St")
        restaurant2 = Restaurant(name="Pepperoni Pizza", address="456 Oak Ave")
        restaurant3 = Restaurant(name="Kiki's Pizza", address="789 Pine Ln")
        db.session.add_all([restaurant1, restaurant2, restaurant3])
        db.session.commit()
        print("Restaurants created.")

        # Create sample Pizzas
        print("Creating pizzas...")
        pizza1 = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Mozzarella, Oregano")
        pizza2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Mozzarella, Pepperoni")
        pizza3 = Pizza(name="Vegetable", ingredients="Dough, Tomato Sauce, Mozzarella, Mushrooms, Olives, Bell Peppers")
        db.session.add_all([pizza1, pizza2, pizza3])
        db.session.commit()
        print("Pizzas created.")

        # Create sample RestaurantPizzas (associations between restaurants and pizzas)
        print("Creating restaurant-pizzas associations...")
        rp1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=10)
        rp2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2, price=12)
        rp3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2, price=11)
        rp4 = RestaurantPizza(restaurant=restaurant2, pizza=pizza3, price=13)
        rp5 = RestaurantPizza(restaurant=restaurant3, pizza=pizza1, price=9)
        rp6 = RestaurantPizza(restaurant=restaurant3, pizza=pizza3, price=15)
        db.session.add_all([rp1, rp2, rp3, rp4, rp5, rp6])
        db.session.commit()
        print("Restaurant-pizzas associations created.")

        print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
