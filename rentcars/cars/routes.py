# -*- coding: utf-8 -*-
"""routes
   Implements the routes for blueprint cars.
"""
import math
import logging
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_security import roles_accepted, current_user
from rentcars import db
from rentcars.models import Cars
from rentcars.cars.forms import AddCar


logger = logging.getLogger("rentcars.cars.routes")
cars = Blueprint('cars', __name__)


@cars.route("/cars", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def show_cars():
    """Show all cars. The application can filter and display a form
    to view the list of clients
    with updated rental cost. Paginate cars. Will be shown 1000 cars per page.
    """
    filter_from = 0
    filter_to = 1_000
    try:
        page = request.args.get('page', 1, type=int)
    except ValueError:
        logger.error(f'You pass {page}. It is wrong type for page number')
        page = 1
    if request.method == 'POST':
        filter_from = math.ceil(float(request.form['cost_from']))
        filter_to = math.ceil(float(request.form['cost_to']))
        cars = Cars.query.filter(Cars.rental_cost.between(filter_from,
                                                          filter_to)).\
            paginate(page=1, per_page=1000)
        return render_template('cars.html', cars=cars, filter_from=filter_from,
                               filter_to=filter_to)
    cars = Cars.query.paginate(page=page, per_page=2)
    logger.info(f'You are on the page={page}')
    return render_template('cars.html', cars=cars, filter_from=filter_from,
                           filter_to=filter_to)


@cars.route("/add_car", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def add_car():
    """
    View for adding car to database. Redirect to page show cars
    """
    form = AddCar()
    if form.validate_on_submit():
        car = Cars(car_number=form.car_number.data,
                   car_description=form.car_description.data,
                   rental_cost=form.rental_cost.data)
        db.session.add(car)
        db.session.commit()
        logger.info(f'Car was added with such param: {form.data} by user='
                    f'{current_user}')
        flash('Your cars was created successful', 'success')
        return redirect(url_for('cars.show_cars'))
    return render_template('add_car.html', form=form, title='Add cars')


@cars.route("/update_car/<car_id>", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def update_car(car_id):
    """
    View for updating information about car. Redirect to page show cars
    """
    car = Cars.query.filter_by(id=car_id).first()
    form = AddCar()
    if form.validate_on_submit():
        car.car_number = form.car_number.data
        car.car_description = form.car_description.data
        car.rental_cost = form.rental_cost.data
        db.session.commit()
        logger.info(f'Car with id={car_id} was updated with such'
                    f' param:{form.data}'
                    f'by user={current_user}')
        flash('Your cars was updated successful', 'success')
        return redirect(url_for('cars.show_cars'))
    if request.method == 'GET':
        form.car_number.data = car.car_number
        form.car_description.data = car.car_description
        form.rental_cost.data = car.rental_cost
    return render_template('add_car.html', form=form, title='Update cars')


@cars.route("/delete_car/<car_id>", methods=['GET', 'POST'])
@roles_accepted('admin', 'worker')
def delete_car(car_id):
    """
    View for deleting client from database.
    """
    car = Cars.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    logger.info(f'Order with id={car_id} was deleted by= {current_user}')
    flash('Car was deleted successfully', 'success')
    return redirect(url_for('cars.show_cars'))
