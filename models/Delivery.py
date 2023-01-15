from sqlalchemy import ForeignKey

from conf import db


class Delivery(db.Model):
    """this class represents the phone numbers table (multi-values attribute)
                Attributes:
                    order_id (int): represents the id of the order,
                    the order_id is the foreign key directly connected to order table
                    address (string): represents the address of gthe delivery
                    name (string): represents the name of the customer
                    del_id (primary key:int): represents the del id
                """

    __tablename__ = "Delivery"
    del_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(100))
    name = db.Column(db.String(100))
    order_id = db.Column(db.Integer, ForeignKey("Order.order_id", ondelete='CASCADE'), nullable=False)

    def __init__(self, **kwargs):
        self.address = kwargs["address"]
        self.name = kwargs["name"]
        self.order_id = kwargs["order_id"]
