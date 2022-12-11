from sqlalchemy import ForeignKey

from conf import db


class Order(db.Model):
    """this class represents the Users table
                Attributes:
                    order_id (primary key:int): represents the id of the unique Order
                    price (string): represents the Order price
                    payment (string): represents the Order payment method
                    emp_id (int): represents the employee id
                    the emp_id is the foreign key directly connected to Employee table
                    delivery (string): represents the employee delivery
                """
    __tablename__ = "Order"
    order_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    price = db.Column(db.Float)
    payment = db.Column(db.String(100))
    emp_id = db.Column(db.Integer, ForeignKey("Employee.emp_id", ondelete='CASCADE'), nullable=False)
    delivery = db.Column(db.Integer)
    OrderToMeal = db.relationship('OrderToMeal', backref="Order", lazy=True, cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        #self.order_id = kwargs["order_id"]
        self.price = kwargs["price"]
        self.payment = kwargs["payment"]
        self.emp_id = kwargs["emp_id"]
        self.delivery = kwargs["delivery"]

