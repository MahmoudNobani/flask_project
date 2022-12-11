import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

JWT_ISSUER = "com.zalando.connexion"
JWT_SECRET = "random"
JWT_LIFETIME_SECONDS = 60
JWT_ALGORITHM = "HS256"

#config file used to specify the main configuration of the program
basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

# app = connexion.App(__name__, specification_dir="./")
# connex_app.add_api("swagger.yml")

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'restaurant.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = 'RANDOM'

db = SQLAlchemy(app)
ma = Marshmallow(app)

