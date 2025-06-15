from server.config import db
from sqlalchemy.ext.associationproxy import association_proxy

class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # Relationships:
    # cascade="all, delete-orphan" ensures that when a Restaurant is deleted,
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade="all, delete-orphan", lazy=True)
    pizzas = association_proxy('restaurant_pizzas', 'pizza')

    def __repr__(self):
        return f'<Restaurant {self.id}: {self.name}>'

    # Serialization method for JSON response
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

