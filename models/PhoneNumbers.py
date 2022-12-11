from sqlalchemy import ForeignKey

from conf import db


class PhoneNumbers(db.Model):
    """this class represents the phone numbers table (multi-values attribute)
                Attributes:
                    emp_id (int): represents the id of the Employees who uses that number,
                    the emp_id is the foreign key directly connected to Employees table
                    type (string): represents the type of number used
                    number (primary key:string): represents the number itself, and its a unique one
                """

    __tablename__ = "PhoneNumbers"
    emp_id = db.Column(db.Integer, ForeignKey("Employee.emp_id", ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(100))
    number = db.Column(db.String(100), primary_key=True)

    def __init__(self, emp_id, **kwargs):
        self.emp_id = emp_id
        self.type = kwargs["type"]
        self.number = kwargs["number"]

