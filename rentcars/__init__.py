from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from rentcars.config import Configuration


db = SQLAlchemy()
migrate = Migrate()



def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    migrate.init_app(app, db)
    from rentcars.models import Cars, Clients, Orders


    from rentcars.orders.routes import orders
    from rentcars.clients.routes import clients
    from rentcars.cars.routes import cars

    app.register_blueprint(orders)
    app.register_blueprint(clients)
    app.register_blueprint(cars)

    return app