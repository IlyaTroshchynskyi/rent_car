# -*- coding: utf-8 -*-
"""routes
   Implements the routes for blueprint orders.
"""
from datetime import datetime
from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_security import roles_accepted
from rentcars import db
from rentcars.models import Orders, Cars, Clients
from rentcars.orders.forms import AddOrder


orders = Blueprint('orders', __name__)


@orders.route('/', methods=['GET', 'POST'])
def index():
    """Show all orders. The application can filter and display a form to view the list of orders
    with updated data. Paginate orders. Will be shown 1000 orders per page.
    """
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        page = 1
    if request.method == 'POST':
        start = datetime.strptime(request.form['calendar_start'],
                                  "%Y-%m-%d").date()
        end = datetime.strptime(request.form['calendar_end'], "%Y-%m-%d").date()
        orders = Orders.query.filter(Orders.date_rent.between(start, end)).\
            paginate(page=1, per_page=1000)
        return render_template('index.html', orders=orders, start=start, end=end)
    start = datetime.strptime('31-12-1970', "%d-%m-%Y").date()
    end = datetime.strptime('31-12-2100', "%d-%m-%Y").date()
    orders = Orders.query.paginate(page=page, per_page=3)
    return render_template('index.html', orders=orders, start=start, end=end)


@orders.route("/add_order", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def add_order():
    """
    View for adding order to database.
    Total cost – total cost of car rental, total cost is calculated as the
    rental time multiplied by car rental cost.
    number_orders - calculated by adding or subtraction 1.
    After adding order redirect to index page
    """
    form = AddOrder()
    if form.validate_on_submit():
        car = Cars.query.filter_by(car_number=form.car_number.
                                   data.car_number).first()
        order = Orders(car_number=form.car_number.data.car_number,
                       car_description=form.car_description.data.car_description,
                       client_passport=form.client_passport.data.passport,
                       date_rent=form.order_date.data,
                       rental_time=form.rental_time.data,
                       rental_cost=car.rental_cost,
                       total_cost=form.rental_time.data * car.rental_cost)
        db.session.add(order)
        db.session.commit()
        car.number_orders += 1
        client = Clients.query.filter_by(passport=form.client_passport.
                                         data.passport).first()
        client.number_orders += 1
        db.session.commit()
        flash('Your order was created successful', 'success')
        return redirect(url_for('orders.index'))
    return render_template('add_order.html', form=form, title='Add order')


@orders.route("/update_order/<order_id>", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def update_order(order_id):
    """
    View for updating order to database.
    """
    order = Orders.query.filter_by(id=order_id).first()
    form = AddOrder()
    first_car_number = order.car_number
    if form.validate_on_submit():
        car = Cars.query.filter_by(car_number=form.car_number.data).first()
        order.car_number = form.car_number.data
        order.car_description = form.car_description.data
        order.client_passport = form.client_passport.data
        order.date_rent = form.order_date.data
        order.rental_time = form.rental_time.data
        order.rental_cost = car.rental_cost
        order.total_cost = (form.rental_time.data * car.rental_cost)
        if first_car_number != form.car_number.data:
            car.number_orders -= 1
            car = Cars.query.filter_by(car_number=first_car_number).first()
            car.number_orders -= 1
            car = Cars.query.filter_by(car_number=form.car_number.data).first()
            car.number_orders += 1
        db.session.commit()
        flash('Your order was updated successful', 'success')
        return redirect(url_for('orders.index'))
    if request.method == 'GET':
        form.car_number.data = order.car_number
        form.car_description.data = order.car_description
        form.client_passport.data = order.client_passport
        form.order_date.data = order.date_rent
        form.rental_time.data = order.rental_time

    return render_template('add_order.html', form=form, title='Update order')


@orders.route("/delete_order/<order_id>", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def delete_order(order_id):
    """
    View for deleting order from database. Have pop up menu for confirmation of deleting.
    """
    order = Orders.query.get_or_404(order_id)
    try:
        order.car.number_orders -= 1
        order.client.number_orders -= 1
    except:
        pass
    db.session.delete(order)
    db.session.commit()
    flash('Your order was deleted successfully', 'success')
    return redirect(url_for('orders.index'))
