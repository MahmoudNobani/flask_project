from conf import db


class Employee(db.Model):
    """this class represents the Users table
                Attributes:
                    emp_id (primary key:int): represents the id of the unique employee
                    first_name (string): represents the employee first name
                    last_name (string): represents the employee last name
                    age (int): represents the employee age
                    gender (string): represents the employee gender
                    salary (float): represents the employee salary
                    position (string): represents the employee position
                    PhoneNumbers : represents the relation between employees table and PhoneNumbers table
                    address : represents the relation between employees and Address table
                    manager : index to represent whether an employee is a manager or not
                    order :  represent the relation between employees and users table
                """
    __tablename__ = "Employee"
    emp_id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(100))
    salary = db.Column(db.Float)
    position = db.Column(db.String(100))
    manager = db.Column(db.Integer)
    address = db.relationship('Address', backref="Employee", lazy=True, cascade="all, delete, delete-orphan")
    PhoneNumbers = db.relationship('PhoneNumbers', backref='Employee', lazy=True, cascade="all, delete, delete-orphan")
    order = db.relationship('Order', backref="Employee", lazy=True, cascade="all, delete, delete-orphan")

    def __init__(self, **kwargs):
        self.emp_id = kwargs["emp_id"]
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.age = kwargs["age"]
        self.manager = kwargs["manager"]
        self.gender = kwargs["gender"]
        self.salary = kwargs["salary"]
        self.position = kwargs["position"]

    def update(self, **kwargs):
        """this function aims to update the Users object, thus the database
                        Args:
                            **kwargs: Arbitrary keyword arguments that represents the emp table main attribute,
                            relation not included
                        Returns:
                            no return value,
                                """
        self.emp_id = kwargs["emp_id"]
        self.first_name = kwargs["first_name"]
        self.last_name = kwargs["last_name"]
        self.age = kwargs["age"]
        self.gender = kwargs["gender"]
        self.salary = kwargs["salary"]
        self.position = kwargs["position"]
        self.manager = kwargs["manager"]

