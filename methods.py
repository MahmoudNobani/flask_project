import json

from flask import request, jsonify
import time

from jose import JWTError
import jwt
from flask import jsonify, request
from werkzeug.exceptions import Unauthorized

from conf import db, JWT_ISSUER, JWT_LIFETIME_SECONDS, JWT_SECRET, JWT_ALGORITHM
from models.Address import Address
from models.Delivery import Delivery
from models.Employee import Employee
from models.Meal import Meal
from models.Order import Order
from models.OrderToMeal import OrderToMeal
from models.PhoneNumbers import PhoneNumbers
from schema import EmpSchema, MealSchema, OrderSchema, OrderToMealSchema


def add_emp_gen(data: json) -> str:
    """ the function aims to add a new emp to the database
        Args:
            data (json): json representation fo the new emp we want to add
        Returns:
            The return value is a string that either represent the success or failure of the addition process
    """
    address_data = {}
    phone_data = {}
    user_data = {}

    for i in data:
        if i == "address":
            address_data[i] = data[i]
        elif i == "PhoneNumbers":
            phone_data[i] = data[i]
        else:
            user_data[i] = data[i]

    # add to the emp object
    new_emp = Employee(**user_data)
    temp = Address(user_data["emp_id"], **address_data["address"])
    new_emp.address.append(temp)

    for i in phone_data["PhoneNumbers"]:
        temp = PhoneNumbers(user_data["emp_id"], **i)
        new_emp.PhoneNumbers.append(temp)

    try:
        db.session.add(new_emp)
        db.session.commit()
        return str(new_emp.emp_id)
    except Exception as err:
        return "unique constrains in user id and phone failed to be applied, " + f"Unexpected {err=}, {type(err)=}"


def get_all_emp() -> json:
    """this function perform a get method with the aim to return all the emp

        Args:
            there is no parameters

        Returns:
            returns a json that contains all the users we have, with 200 status code

        """

    people = Employee.query.all()
    schema = EmpSchema(many=True)
    return jsonify(schema.dump(people)), 200


def add_emp() -> json:
    """this function adds a new emp to the database with the help of add_user_gen
        Args:
            this function doesn't take any parameters

        Returns:
            returns the new emp data as a json on success with 201 status code or
            an error message as a json representing what went wrong with 400 status code

        """
    new_emp = request.json
    validation = add_emp_gen(new_emp)
    print(validation)
    if validation[:6] == "unique":
        return jsonify(validation), 400
    new_emp_data = Employee.query.filter(int(validation) == Employee.emp_id)
    schema = EmpSchema(many=True)
    return jsonify(schema.dump(new_emp_data)), 201


def del_emp(emp_id: str) -> json:
    """given the id, this function perform the delete operation on it

        Args:
             emp_id (string): represents the id of the user we want to delete
        Returns:
            a json that represents whether the operation was successful or not
            or an error message representing what went wrong

        """

    try:
        deleted_users = Employee.query.filter(int(emp_id) == Employee.emp_id).delete()
        PhoneNumbers.query.filter(int(emp_id) == PhoneNumbers.emp_id).delete()
        Address.query.filter(int(emp_id) == Address.emp_id).delete()
        if deleted_users > 0:
            db.session.commit()
            return jsonify("delete was successful"), 202
        else:
            return jsonify("user not found"), 404
    except Exception as err:
        return jsonify("entered id has to be integer, " + f"Unexpected {err=}, {type(err)=}"), 400


def get_emp_with_id(emp_id: str) -> json:
    """this function Return the emp with the given id_.

        Args:
            emp_id (string): represents the id_ of the emp we want to search

        Returns:
            this function returns the data of the emp with the given id_ as a json wih 200 status code
            or an error message

        """
    try:
        people = Employee.query.filter(int(emp_id) == Employee.emp_id)
        schema = EmpSchema(many=True)
        if not schema.dump(people):
            return jsonify("user was not found"), 404
        return schema.dump(people), 200
    except Exception as err:
        return jsonify("entered id has to be integer, " + f"Unexpected {err=}, {type(err)=}"), 400


def update_emp(emp_id: str) -> json:
    """given the id, this function perform the update operation on it with the help of
    update_emp_gen function

        Args:
             emp_id (string): represents the id of the emp we want to update
        Returns:
            json message that represents whether the operation was successful or not

        """
    updated_user = request.json
    updated_user["emp_id"] = int(emp_id)
    try:  # check if exists
        user = db.session.execute(db.select(Employee).filter(Employee.emp_id == int(emp_id))).one()
    except Exception as err:
        return jsonify(f"Unexpected {err=}, {type(err)=}"), 404

    update_emp_gen(user, updated_user)
    db.session.commit()
    return jsonify("update successful"), 201


def update_emp_gen(user: object, updated_user: json) -> json:
    """ the function aims to update the emp object
            Args:
                user (object): represents the emp we want to update
                updated_user (json): json representation of the updated information
            Returns:
                    there is no return value
                        """

    address_data = {}
    phone_data = {}
    user_data = {}

    for i in updated_user:
        if i == "address":
            address_data[i] = updated_user[i]
        elif i == "PhoneNumbers":
            phone_data[i] = updated_user[i]
        else:
            user_data[i] = updated_user[i]

    # update user date
    user[0].update(**user_data)
    # update the phone numbers data
    user[0].PhoneNumbers.clear()
    for i in phone_data["PhoneNumbers"]:
        temp2 = PhoneNumbers(user_data["emp_id"], **i)
        user[0].PhoneNumbers.append(temp2)
    # update the address data
    user[0].address[0].update(user_data["emp_id"], **address_data["address"])


def add_meal() -> json:
    """ the function add a new meal for the menu
                Args:
                    there is no arguments
                Returns:
                        there is no return value
            """
    new_meal = request.json
    meal_object = Meal(**new_meal)
    meal_id = new_meal["meal_id"]
    print(meal_id)
    try:
        db.session.add(meal_object)
        db.session.commit()
        new_meal_data = Meal.query.filter(meal_id == Meal.meal_id)
        schema = MealSchema(many=True)
        return jsonify(schema.dump(new_meal_data)), 201
    except Exception as err:
        return "unique constrains in meal id failed to be applied, " + f"Unexpected {err=}, {type(err)=}", 400


def get_all_meals() -> json:
    """this function perform a get method with the aim to return all the meals

        Args:
            there is no parameters

        Returns:
            returns a json that contains all the meals we have available, with 200 status code

        """

    # meals = Meal.query.filter(Meal.remaining > 0).all()
    meals = Meal.query.all()
    schema = MealSchema(many=True)
    return jsonify(schema.dump(meals)), 200


def update_meal(meal_id: str) -> json:
    """given the id, this function perform the update operation on a meal

        Args:
             meal_id (string): represents the id of the meal we want to update
        Returns:
            json message that represents whether the operation was successful or not with 201 status code
            404 status code is returned if a meal doesn't exist

        """
    updated_meal = request.json
    updated_meal["meal_id"] = int(meal_id)
    try:  # check if exists
        old_meal = db.session.execute(db.select(Meal).filter(Meal.meal_id == int(meal_id))).one()
    except Exception as err:
        return jsonify(f"Unexpected {err=}, {type(err)=}"), 404

    old_meal[0].update(**updated_meal)
    db.session.commit()
    return jsonify("update successful"), 201


def add_order() -> json:
    """this function adds a new order
            Args:
                this function doesn't take any parameters

            Returns:
                returns the new order number and price as a json on success with 201 status code or
                an error message as a json representing what went wrong with 400 status code or
                404 status code if the emp or a meal doesn't exist

            """

    # read the new order data
    new_order = request.json

    order_info = {}
    meals_id = {}
    total_price = 0

    # separate meals and order info
    for i in new_order:
        if i == "Meals":
            meals_id[i] = new_order[i]
        else:
            order_info[i] = new_order[i]

    # check if the entered user id exists.
    people = Employee.query.filter(int(order_info['Order']["emp_id"]) == Employee.emp_id)
    schema = EmpSchema(many=True)
    if not schema.dump(people):
        return jsonify("user was not found"), 404

    try:
        # update the sales and remaining parameters in meals and calculate the price
        for i in meals_id["Meals"]:
            meals = db.session.execute(db.select(Meal).filter(Meal.meal_id == i)).one()
            if meals[0].remaining == 0:
                return jsonify("there is no ", meals[0].name, "please order something else"), 404
            else:
                meals[0].update_sales(meals[0].sales + 1, meals[0].remaining - 1)
            total_price += meals[0].price
        # print(total_price)

        # add to order
        order_info['Order']["price"] = total_price
        # print(order_info['Order'])
        order_object = Order(**order_info['Order'])
        db.session.add(order_object)
        db.session.commit()

        # add to OrderToMeal table
        print(order_object.order_id)
        for i in meals_id["Meals"]:
            temp = OrderToMeal(order_object.order_id, i)
            db.session.add(temp)

        db.session.commit()

        return jsonify("order ", order_object.order_id, " was added, total price: ", total_price), 201
    except Exception as err:
        return "unique constrains in meal id failed to be applied, " + f"Unexpected {err=}, {type(err)=}", 400


def update_order(order_id: str) -> json:
    """given the id, this function perform the update operation on an order

            Args:
                 order_id (string): represents the id of the order we want to update
            Returns:
                json message that represents whether the operation was successful or not with 201 status code
            404 status code is returned if a meal/order doesn't exist
        """
    new_order = request.json

    order_info = {}
    meals_id = {}
    total_price = 0

    # separate meals from order
    for i in new_order:
        if i == "Meals":
            meals_id[i] = new_order[i]
        else:
            order_info[i] = new_order[i]

    # get all old meals and old orders
    old_meals = []
    old_orders = db.session.execute(db.select(OrderToMeal).filter(OrderToMeal.order_id == int(order_id)))
    schema = OrderToMealSchema(many=True)
    if not schema.dump(old_orders):
        return jsonify("order was not found"), 404

    old_orders = db.session.execute(db.select(OrderToMeal).filter(OrderToMeal.order_id == int(order_id)))
    for i in old_orders:
        old_meals.append(i[0].meal_id)

    try:
        # update sales and remaining for old and new meals ordered
        for i in old_meals:
            meals = db.session.execute(db.select(Meal).filter(Meal.meal_id == i)).one()
            meals[0].update_sales(meals[0].sales - 1, meals[0].remaining + 1)

        for i in meals_id["Meals"]:
            meals = db.session.execute(db.select(Meal).filter(Meal.meal_id == i)).one()
            if meals[0].remaining == 0:
                return jsonify("there is no ", meals[0].name, "please order something else"), 404
            else:
                meals[0].update_sales(meals[0].sales + 1, meals[0].remaining - 1)
            total_price += meals[0].price

        # delete the orders in OrderToMeal table
        OrderToMeal.query.filter(OrderToMeal.order_id == int(order_id)).delete()

        # get order table object and update
        old_order_from_orderT = db.session.execute(db.select(Order).filter(Order.order_id == int(order_id))).one()
        order_info['Order']["price"] = total_price
        print(order_info["Order"])
        old_order_from_orderT[0].update(**order_info["Order"])

        # add new orders to OrderToMeal table
        for i in meals_id["Meals"]:
            temp = OrderToMeal(order_id, i)
            db.session.add(temp)

        check = Order.query.filter(int(order_id) == Order.order_id).with_entities(Order.delivery)
        x = db.session.execute(check).first()
        if int(x[0]) == 0:
            rm_deli_request(int(order_id))

        # commit everything
        db.session.commit()

        return jsonify("update done"), 201
    except Exception as err:
        return "meal not found, " + f"Unexpected {err=}, {type(err)=}", 404


def delete_order(order_id: str) -> json:
    """given the id, this function perform the delete operation on an order

            Args:
                 order_id (string): represents the id of the order we want to delete
            Returns:
                json message that represents whether the operation was successful or not with 201 status code
            404 status code is returned if a meal/order doesn't exist
        """

    # get all old meals and old orders
    old_meals = []
    old_orders = db.session.execute(db.select(OrderToMeal).filter(OrderToMeal.order_id == int(order_id)))
    print(old_orders)
    schema = OrderToMealSchema(many=True)

    #print(schema.dump(old_orders))

    if not schema.dump(old_orders):
        return jsonify("order was not found"), 404

    old_orders = db.session.execute(db.select(OrderToMeal).filter(OrderToMeal.order_id == int(order_id)))
    for i in old_orders:
        print("i:",i)
        print("i[0]:",i[0])
        print(i[0].meal_id)
        old_meals.append(i[0].meal_id)

    #print(old_meals)

    try:

        # check delivery and delete
        check = Order.query.filter(int(order_id) == Order.order_id).with_entities(Order.delivery)
        x = db.session.execute(check).first()
        if int(x[0]) == 1:
            rm_deli_request(int(order_id))

        # update sales and remaining for old and new meals ordered
        for i in old_meals:
            meals = db.session.execute(db.select(Meal).filter(Meal.meal_id == i)).one()
            meals[0].update_sales(meals[0].sales - 1, meals[0].remaining + 1)

        # delete the orders in OrderToMeal table
        OrderToMeal.query.filter(OrderToMeal.order_id == int(order_id)).delete()
        Order.query.filter(int(order_id) == Order.order_id).delete()

        # commit everything
        db.session.commit()

        return jsonify("delete done"), 202
    except Exception as err:
        return f"Unexpected {err=}, {type(err)=}", 404


def get_all_orders() -> json:
    """this function perform a get method with the aim to return all the orders

            Args:
                there is no parameters

            Returns:
                returns a json that contains all the orders made, with 200 status code

            """
    orders = Order.query.all()
    schema = OrderSchema(many=True)
    return jsonify(schema.dump(orders)), 200


def order_handled_by_emp(emp_id: str) -> json:
    """this function perform a get method with the aim to return all the orders handled by this employee

                Args:
                    there is no parameters

                Returns:
                    returns a json that contains all the orders handled, with 200 status code

                """

    people = Employee.query.filter(int(emp_id) == Employee.emp_id)
    schema = EmpSchema(many=True)
    if not schema.dump(people):
        return jsonify("user was not found"), 404

    # count = Order.query.filter(int(emp_id) == Order.emp_id).count()
    orders = Order.query.filter(int(emp_id) == Order.emp_id)
    schema = OrderSchema(many=True)
    return jsonify(schema.dump(orders)), 200


def add_deli() -> json:
    """ the function add a new del infor
                Args:
                    there is no arguments
                Returns:
                     this function returns 404 status code if order doesn't exist
                     400 is not supported
                     and 201 if the operation is successful
            """
    del_info = request.json
    order_id = del_info["order_id"]
    check = Order.query.filter(int(order_id) == Order.order_id).with_entities(Order.delivery)
    x = db.session.execute(check).first()
    if x is None:
        return jsonify("order doesnt exists"), 404
    if int(x[0]) == 0:
        return jsonify("this order doesnt support delivery, please update it"), 400
    else:
        if db.session.execute(db.select(Delivery).filter(int(order_id) == Delivery.order_id)).first() is None:
            return jsonify(add_deli_gen(del_info)), 201
        else:
            rm_deli_request(int(order_id))
            return jsonify(add_deli_gen(del_info)), 201


def update_deli(order_id: str) -> json:
    """ the function add a new del infor
                Args:
                    order_id(str): parameter that represents the order id
                Returns:
                     this function returns 404 status code if order doesn't exist
                     400 is not supported
                     and 201 if the operation is successful
            """
    del_info = request.json
    del_info["order_id"] = int(order_id)
    check = Order.query.filter(int(order_id) == Order.order_id).with_entities(Order.delivery)
    x = db.session.execute(check).first()
    if x is None:
        return jsonify("order doesnt exists"), 404
    if int(x[0]) == 0:
        rm_deli_request(int(order_id))
        db.session.commit()
        return jsonify("this order doesnt support delivery, please update it"), 400
    else:
        if db.session.execute(db.select(Delivery).filter(int(order_id) == Delivery.order_id)).first() is None:
            return jsonify(add_deli_gen(del_info)), 201
        else:
            rm_deli_request(int(order_id))
            return jsonify(add_deli_gen(del_info)), 201


def add_deli_gen(del_info: json) -> str:
    """ the function add a new del info to the database directly
                    Args:
                        del_info(json): parameter that represents the delivery infor
                    Returns:
                         return and info msg
                """
    del_object = Delivery(**del_info)
    db.session.add(del_object)
    db.session.commit()
    return "delivery was added"


def rm_deli_request(order_id: int):
    """ the function remove a del info from the database directly
                    Args:
                        order_id(int): parameter that represents the order id
                    Returns:
                        no return value
                """
    Delivery.query.filter(order_id == Delivery.order_id).delete()


def generate_token(emp_id: int) -> str:
    """ the function is used to create authentication token
                Args:
                    emp_id (int): represents the id of the user who wants the token
                Returns:
                        token (str)
                            """

    print(emp_id)
    emp = db.session.execute(db.select(Employee).filter(Employee.emp_id == int(emp_id))).one()
    if emp[0].manager == 1:
        timestamp = _current_timestamp()
        payload = {
            "iss": JWT_ISSUER,
            "iat": int(timestamp),
            "exp": int(timestamp + JWT_LIFETIME_SECONDS),
            "sub": str(emp_id),
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM), 200
    else:
        return jsonify("not a manager, can produce a token"), 401


def decode_token(token: str):
    """ the function is used to decode authentication token
                Args:
                    token (str): represents the token
                Returns:
                    either a dictionary that represents the decoded token or an error exception
                            """
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized from e
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")


def _current_timestamp() -> int:
    """ the function is used to get current timestamp
            Args:
                no arguments
            Returns:
                return the current time
                        """
    return int(time.time())


def emp_names_sold_meals(meal_id: str) -> json:
    """ the function is performs a query where it can get the name of each employee who sold the entered meal id
                Args:
                   meal_id(str) : represents the name of the meal we will use
                Returns:
                    returns the name of employees with a status code of 200
                            """
    answer = db.session.query(
        Employee, Meal, Order, OrderToMeal
    ).filter(
        Employee.emp_id == Order.emp_id,
    ).filter(
        OrderToMeal.order_id == Order.order_id,
    ).filter(
        OrderToMeal.meal_id == Meal.meal_id,
    ).filter(
        Meal.meal_id == int(meal_id),
    ).all()

    emp_name = {}
    for i in answer:
        s = i[0].first_name + " " + i[0].last_name
        if s in emp_name:
            emp_name[s] += 1
            continue
        emp_name[s] = 1

    # print(emp_name)
    return jsonify(emp_name), 200


def meals_delivered() -> json:
    """ the function is performs a query where it can get the name of each employee who sold the entered meal id
                Args:
                   meal_id(str) : represents the name of the meal we will use
                Returns:
                    returns the name of employees with a status code of 200
                            """
    answer = db.session.query(
        Delivery, Meal, Order, OrderToMeal
    ).filter(
        Meal.meal_id == OrderToMeal.meal_id,
    ).filter(
        OrderToMeal.order_id == Order.order_id,
    ).filter(
        Order.order_id == Delivery.order_id
    ).filter(
        Order.delivery == 1,
    ).all()

    print(answer)

    meals_name = {}
    for i in answer:
        s = i[1].name
        if s in meals_name:
            meals_name[s] += 1
            continue
        meals_name[s] = 1

    return jsonify(meals_name), 200
