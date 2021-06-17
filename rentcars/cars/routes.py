import math
from flask import Blueprint, request, render_template, redirect, url_for, flash
from rentcars import db
from rentcars.models import Cars
from rentcars.cars.forms import AddCar


cars = Blueprint('cars', __name__)


@cars.route("/cars", methods=['GET', 'POST'])
def show_cars():
    filter_from = 0
    filter_to = 1_000
    try:
        page = request.args.get('page', 1, type=int)
    except:
        page = 1
    if request.method == 'POST':
        filter_from = math.ceil(float(request.form['cost_from']))
        filter_to = math.ceil(float(request.form['cost_to']))
        cars = Cars.query.filter(Cars.rental_cost.between(filter_from,
                                                          filter_to)).paginate(page=1, per_page=1000)
        return render_template('cars.html', cars=cars, filter_from=filter_from,
                               filter_to=filter_to)
    cars = Cars.query.paginate(page=page, per_page=2)
    return render_template('cars.html', cars=cars, filter_from=filter_from,
                               filter_to=filter_to)


@cars.route("/add_car", methods=['GET', 'POST'])
def add_car():
    form = AddCar()
    if form.validate_on_submit():
        car = Cars(car_number=form.car_number.data,
                       car_description=form.car_description.data,
                       rental_cost=form.rental_cost.data)
        db.session.add(car)
        db.session.commit()
        flash('Your car was created successful', 'success')
        return redirect(url_for('cars.show_cars'))
    return render_template('add_car.html', form=form, title='Add car')


@cars.route("/update_car/<car_id>", methods=['GET', 'POST'])
def update_car(car_id):
    car = Cars.query.filter_by(id=car_id).first()
    form = AddCar()
    if form.validate_on_submit():
        car.car_number = form.car_number.data
        car.car_description = form.car_description.data
        car.rental_cost = form.rental_cost.data
        db.session.commit()
        flash('Your car was updated successful', 'success')
        return redirect(url_for('cars.show_cars'))
    if request.method == 'GET':
        form.car_number.data = car.car_number
        form.car_description.data = car.car_description
        form.rental_cost.data = car.rental_cost
    return render_template('add_car.html', form=form, title='Update car')


@cars.route("/delete_car/<car_id>", methods=['GET', 'POST'])
def delete_car(car_id):
    car = Cars.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car was deleted successfully', 'success')
    return redirect(url_for('cars.show_cars'))