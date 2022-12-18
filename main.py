from conf import app, connex_app, db
from models import Employee, Address, PhoneNumbers, Order, Meal, Delivery, OrderToMeal

connex_app.add_api("open_api/swagger.yml")

if __name__ == '__main__':
    app.app_context().push()
    #db.drop_all()
    #db.create_all()


    #db.session.commit()
    app.run(host="0.0.0.0", port=8000, debug=True)
