from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import declarative_base

from conf import db


class OrderToMeal(db.Model):
    """this class represents the address table (multi-values attribute)
            Attributes:
                emp_id (primary key:int): represents the Employee of the user that lives in that address,
                the emp_id is the foreign key directly connected to Employee table
                street_address (string): represents the street address
                city (string): represents the city
                state (string): represents the state
                postal_code (string): represents the postal_code
            """
    __tablename__ = "OrderToMeal"
    gen_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, ForeignKey("Order.order_id", ondelete='CASCADE'))
    meal_id = db.Column(db.Integer, ForeignKey("Meal.meal_id", ondelete='CASCADE'))

    def __init__(self, order_id, meal_id):
        self.order_id = order_id
        self.meal_id = meal_id

    def printALL(self):
        print("order id:",self.order_id," ,meal id:",self.meal_id)

