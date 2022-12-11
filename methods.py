import json

from flask import request, jsonify

from conf import db
from models.Address import Address
from models.Employee import Employee
from models.Meal import Meal
from models.Order import Order
from models.OrderToMeal import OrderToMeal
from models.PhoneNumbers import PhoneNumbers
from schema import EmpSchema, MealSchema


def add_user_gen(data: json) -> str:
    """ the function aims to add a new user to the database
        Args:
            data (json): json representation fo the new user we want to add
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


def get_all_users() -> json:
    """this function perform a get method with the aim to return all the users

        Args:
            there is no parameters

        Returns:
            returns a json that contains all the users we have, with 200 status code

        """

    people = Employee.query.all()
    schema = EmpSchema(many=True)
    print("x")
    return jsonify(schema.dump(people)), 200


def add_user() -> json:
    """this function adds a new user to teh database with the help of add_user_gen
        Args:
            this function doesn't take any parameters

        Returns:
            returns the new user data as a json on success with 201 status code or
            an error message as a json representing what went wrong with 400 status code

        """
    new_user = request.json
    validation = add_user_gen(new_user)
    print(validation)
    if validation[:6] == "unique":
        return jsonify(validation), 400
    new_user_data = Employee.query.filter(int(validation) == Employee.emp_id)
    schema = EmpSchema(many=True)
    return jsonify(schema.dump(new_user_data)), 201


def del_user(emp_id: str) -> json:
    """given the id, this function perform the delete operation on it

        Args:
             user_id (string): represents the id of the user we want to delete
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


def get_user_with_id(emp_id: str) -> json:
    """this function Return the user with the given id_.

        Args:
            user_id (string): represents the id_ of the user we want to search

        Returns:
            this function returns the data of the user with the given id_ as a json wih 200 status code
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


def update_user(emp_id: str) -> json:
    """given the id, this function perform the update operation on it with the help of
    update_user_gen function

        Args:
             emp_id (string): represents the id of the user we want to update
        Returns:
            json message that represents whether the operation was successful or not

        """
    updated_user = request.json
    updated_user["emp_id"] = int(emp_id)
    try:  # check if exists
        user = db.session.execute(db.select(Employee).filter(Employee.emp_id == int(emp_id))).one()
    except Exception as err:
        return jsonify(f"Unexpected {err=}, {type(err)=}"), 404

    update_user_gen(user, updated_user)
    db.session.commit()
    return jsonify("update successful"), 201


def update_user_gen(user: object, updated_user: json) -> json:
    """ the function aims to update the user object
            Args:
                user (object): represents the user we want to update
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
        return "unique constrains in user id and phone failed to be applied, " + f"Unexpected {err=}, {type(err)=}"


def get_all_meals() -> json:
    """this function perform a get method with the aim to return all the users

        Args:
            there is no parameters

        Returns:
            returns a json that contains all the users we have, with 200 status code

        """

    meals = Meal.query.all()
    schema = MealSchema(many=True)
    print("x")
    return jsonify(schema.dump(meals)), 200


def update_meal(meal_id: str) -> json:
    """given the id, this function perform the update operation on it with the help of
    update_user_gen function

        Args:
             meal_id (string): represents the id of the meal we want to update
        Returns:
            json message that represents whether the operation was successful or not

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
    new_order = request.json

    order_info = {}
    meals_id = {}
    total_price = 0

    for i in new_order:
        if i == "Meals":
            meals_id[i] = new_order[i]
        else:
            order_info[i] = new_order[i]

    for i in meals_id["Meals"]:
        meals = db.session.execute(db.select(Meal).filter(Meal.meal_id == i)).one()
        if meals[0].remaining == 0:
            return jsonify("there is no ", meals[0].name, "please order something else"), 404
        else:
            meals[0].update_sales(meals[0].sales + 1, meals[0].remaining - 1)
        total_price += meals[0].price
    print(total_price)

    order_info['Order']["price"] = total_price
    print(order_info['Order'])
    order_object = Order(**order_info['Order'])
    db.session.add(order_object)
    db.session.commit()

    print(order_object.order_id)
    for i in meals_id["Meals"]:
        temp = OrderToMeal(order_object.order_id, i)
        db.session.add(temp)

    db.session.commit()

    return jsonify("order ", order_object.order_id, " was added, total price: ", total_price), 201
