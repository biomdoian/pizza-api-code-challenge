from server.config import db
from sqlalchemy.ext.associationproxy import association_proxy

class Pizza(db.Model):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # 'pizza_restaurant_pizzas' is the backref from RestaurantPizza to Pizza
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', lazy=True)
    restaurants = association_proxy('restaurant_pizzas', 'restaurant')

    def __repr__(self):
        return f'<Pizza {self.id}: {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

