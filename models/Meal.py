from sqlalchemy import ForeignKey

from conf import db


class Meal(db.Model):
    """this class represents the Users table
                Attributes:
                    meal_id (primary key:int): represents the id of the unique Meal
                    name (string): represents the Meal name
                    remaining (int): represents the Meal remaining in storage
                    sales (int): represents the meal sales
                    price (float): represents the meal price
                """
    __tablename__ = "Meal"
    meal_id = db.Column(db.Integer, unique=True, primary_key=True)
    price = db.Column(db.Float)
    name = db.Column(db.String(100))
    remaining = db.Column(db.Integer)
    sales = db.Column(db.Integer)
    OrderToMeal = db.relationship('OrderToMeal', backref="Meal", lazy=True, cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        self.meal_id = kwargs["meal_id"]
        self.price = kwargs["price"]
        self.name = kwargs["name"]
        self.remaining = kwargs["remaining"]
        self.sales = kwargs["sales"]

    def update(self, **kwargs):
        """this function aims to update the meAL object, thus the database
                        Args:
                            **kwargs: Arbitrary keyword arguments that represents the meal table main attribute,
                            relation not included
                        Returns:
                            no return value,
                                """
        self.meal_id = kwargs["meal_id"]
        self.price = kwargs["price"]
        self.name = kwargs["name"]
        self.remaining = kwargs["remaining"]
        self.sales = kwargs["sales"]

    def update_sales(self,sales,remaining):
        self.remaining = remaining
        self.sales = sales

    def __str__(self):
        print("meal_id = ",self.meal_id,",price = ",self.price,",name = ",self.name,",remaining = ",self.remaining,",sales = ",self.sales)




