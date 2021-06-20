from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, current_user, Security
from flask_login import LoginManager
from rentcars.config import Configuration


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Rentcars', url='/admin', base_template='admin/update_admin_link.html')
security = Security()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'


def create_app(config_class=Configuration):
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    migrate.init_app(app, db)

    from rentcars.models import Cars, Clients, Orders, User, Role

    class ClientView(ModelView):
        can_export = True
        page_size = 1

    class UsersView(ModelView):
        column_list = ['username', 'email', 'roles']
        form_excluded_columns = ['password']
        can_create = False

    class RolesView(ModelView):

        form_excluded_columns = ['users']

    class MainIndexLink(MenuLink):
        def get_url(self):
            return url_for("orders.index")

    admin.init_app(app=app)
    login_manager.init_app(app)

    admin.add_view(ModelView(Cars, db.session, endpoint='cars_admin'))
    admin.add_view(ClientView(Clients, db.session, endpoint='clients_admin'))
    admin.add_view(ModelView(Orders, db.session, endpoint='orders_admin'))
    admin.add_view(RolesView(Role, db.session, endpoint='roles'))
    admin.add_view(UsersView(User, db.session, endpoint='admin_users'))
    admin.add_link(MainIndexLink(name='Rent cars', category=''))

    from rentcars.orders.routes import orders
    from rentcars.clients.routes import clients
    from rentcars.cars.routes import cars
    from rentcars.users.routes import users

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)


    app.register_blueprint(orders)
    app.register_blueprint(clients)
    app.register_blueprint(cars)
    app.register_blueprint(users)

    return app