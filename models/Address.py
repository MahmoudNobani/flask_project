from sqlalchemy import ForeignKey

from conf import db


class Address(db.Model):
    """this class represents the address table (multi-values attribute)
            Attributes:
                emp_id (primary key:int): represents the Employee of the user that lives in that address,
                the emp_id is the foreign key directly connected to Employee table
                street_address (string): represents the street address
                city (string): represents the city
                state (string): represents the state
                postal_code (string): represents the postal_code
            """
    __tablename__ = "Address"
    emp_id = db.Column(db.Integer, ForeignKey("Employee.emp_id", ondelete='CASCADE'), primary_key=True)
    street_address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(100))

    def __init__(self, emp_id, **kwargs):
        self.emp_id = emp_id
        self.street_address = kwargs["street_address"]
        self.city = kwargs["city"]
        self.state = kwargs["state"]
        self.postal_code = kwargs["postal_code"]

    def update(self, emp_id, **kwargs):
        """this function aims to update the address object, thus the database
                Args:
                    emp_id (int): represents the id of the emp.
                    **kwargs: Arbitrary keyword arguments that represents the address table attribute
                Returns:
                    no return value
                        """
        self.emp_id = emp_id
        self.street_address = kwargs["street_address"]
        self.city = kwargs["city"]
        self.state = kwargs["state"]
        self.postal_code = kwargs["postal_code"]

