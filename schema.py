from marshmallow import Schema, fields


class PhoneSchema(Schema):
    """this class the schema for the PhoneNumbers table
                    Attributes:
                        emp_id (string): represents the id of the unique emp
                        type (string): represents the phone type
                        number (string): represents the phone number
                    """
    emp_id = fields.String()
    type = fields.String()
    number = fields.String()


class AddSchema(Schema):
    """this class the schema for the Address table
                        Attributes:
                            emp_id (string): represents the id of the unique emp
                            street_address (string): represents the street_address
                            city (string): represents the city
                            state (string): represents the state
                            postal_code (string): represents the postal_code
                        """
    emp_id = fields.String()
    street_address = fields.String()
    city = fields.String()
    state = fields.String()
    postal_code = fields.String()


class OrderToMealSchema(Schema):
    order_id = fields.String()
    meal_id = fields.String()
    # Orders = fields.Nested(OrderSchemaOG(only=("emp_id", "delivery","payment")), many=True)
    # Meals = fields.Nested(MealSchemaOG(only=("name", "price")), many=True)


class MealSchema(Schema):
    """this class the schema for the Address table
                        Attributes:
                            meal_id (primary key:int): represents the id of the unique Meal
                            name (string): represents the Meal name
                            remaining (int): represents the Meal remaining in storage
                            sales (int): represents the meal sales
                            price (float): represents the meal price
                        """
    meal_id = fields.String()
    name = fields.String()
    remaining = fields.String()
    sales = fields.String()
    price = fields.String()
    # Orders = fields.Nested(OrderToMealSchema(only=("order_id", "meal_id")), many=True)


class OrderSchema(Schema):
    """this class the schema for the Address table
                        Attributes:
                            order_id (primary key:int): represents the id of the unique Order
                            price (string): represents the Order price
                            payment (string): represents the Order payment method
                            emp_id (int): represents the employee id
                            the emp_id is the foreign key directly connected to Employee table
                            delivery (string): represents the employee delivery
                        """
    order_id = fields.String()
    price = fields.String()
    payment = fields.String()
    emp_id = fields.String()
    delivery = fields.String()
    OrderToMeal = fields.Nested(OrderToMealSchema(only=("meal_id",)), many=True)


class delSchema(Schema):
    """this class the schema for the Address table
                        Attributes:
                            order_id (int): represents the id of the order,
                            the order_id is the foreign key directly connected to order table
                            address (string): represents the address of gthe delivery
                            name (string): represents the name of the customer
                            del_id (primary key:int): represents the del id
                        """
    order_id = fields.String()
    name = fields.String()
    address = fields.String()
    del_id = fields.String()


class OrderToMealSchema(Schema):
    """this class the schema for the Address table
                        Attributes:
                            order_id (primary keyint): represents the id of the order,
                            the order_id is the foreign key directly connected to order table
                            meal_id (primary key:int): represents the id of the meal,
                            the meal_id is the foreign key directly connected to meal table
                        """
    gen_id = fields.String()
    order_id = fields.String()
    meal_id = fields.String()


class EmpSchema(Schema):
    """this class represents the Users table schema
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
    emp_id = fields.String()
    first_name = fields.String()
    last_name = fields.String()
    age = fields.String()
    gender = fields.String()
    salary = fields.String()
    position = fields.String()
    manager = fields.String()
    PhoneNumbers = fields.Nested(PhoneSchema(only=("type", "number")), many=True)
    address = fields.Nested(AddSchema(only=("street_address", "city", "state", "postal_code")), many=True)
    # order = fields.Nested(AddSchema(only="order_id"), many=True)
