# -*- coding: utf-8 -*-
"""config
   Implements initialization of application.
"""
import logging
from flask import Flask, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore, current_user, Security
from flask_login import LoginManager
from flask_mail import Mail
from rentcars.config import Configuration, init_logger


db = SQLAlchemy()
migrate = Migrate()
admin = Admin(name='Rentcars', url='/admin',
              base_template='admin/update_admin_link.html')
security = Security()
login_manager = LoginManager()
login_manager.login_view = 'users.login_page'
mail = Mail()


class AdminMixin:
    """
    In the navigation menu, components that are not accessible to a
    user who doesn't have role admin
    """
    def is_accessible(self):
        return current_user.has_role('admin')

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('users.login_page', next=request.url))


class ClientView(AdminMixin, ModelView):
    """Customization admin panel. Can export tables into csv file and one item
    placed on client view
    """
    can_export = True
    page_size = 1


class UsersView(AdminMixin, ModelView):
    """Customization admin panel. Delete column with password to avoid look through password.
    Delete opportunity create new users
    """
    column_list = ['username', 'email', 'roles']
    form_excluded_columns = ['password']
    can_create = False


class RolesView(AdminMixin, ModelView):
    """Customization admin panel. Delete column with users.
    """
    form_excluded_columns = ['users']


class MainIndexLink(MenuLink):
    """Customization admin panel. Added link to rentcars page.
    """
    def get_url(self):
        return url_for("orders.index")


def create_app(config_class=Configuration):
    """Create and configure an instance of the Flask application.
    Args:
        config_class (class): Class with configuration
    Returns:
        app (obj): Return application
    """

    init_logger('rentcars')
    logger = logging.getLogger("rentcars.__init__")
    logger.info('Start creating app rentcars')
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    migrate.init_app(app, db)

    from rentcars.models import Cars, Clients, Orders, User, Role

    admin.init_app(app=app)
    login_manager.init_app(app)
    mail.init_app(app)

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
    from rentcars.errors.handlers import errors

    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, user_datastore)

    app.register_blueprint(orders)
    app.register_blueprint(clients)
    app.register_blueprint(cars)
    app.register_blueprint(users)
    app.register_blueprint(errors)

    logger.info('Finished creating app rentcars')

    return app
