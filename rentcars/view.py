from app import app
from flask import render_template, url_for, redirect, flash, request
from models import Orders, Cars, Clients
from app import db
from forms import AddOrder, AddCar, AddClient


@app.route('/')
def index():
    orders = Orders.query.all()
    return render_template('index.html', orders=orders)


@app.route("/add_order", methods=['GET', 'POST'])
def add_order():
    form = AddOrder()
    if form.validate_on_submit():
        car = Cars.query.filter_by(car_number=form.car_number.data).first()
        order = Orders(car_number=form.car_number.data,
                       car_description=form.car_description.data,
                       client_passport=form.client_passport.data,
                       date_rent=form.order_date.data,
                       rental_time=form.rental_time.data,
                       rental_cost=car.rental_cost,
                       total_cost=form.rental_time.data * car.rental_cost)
        db.session.add(order)
        db.session.commit()
        car.number_orders += 1
        client = Clients.query.filter_by(passport=form.client_passport.data).first()
        client.number_orders += 1
        db.session.commit()
        flash('Your order was created successful', 'success')
        return redirect(url_for('index'))
    return render_template('add_order.html', form=form, title='Add order')


@app.route("/update_order/<order_id>", methods=['GET', 'POST'])
def update_order(order_id):
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
        return redirect(url_for('index'))
    if request.method == 'GET':
        form.car_number.data = order.car_number
        form.car_description.data = order.car_description
        form.client_passport.data = order.client_passport
        form.order_date.data = order.date_rent
        form.rental_time.data = order.rental_time

    return render_template('add_order.html', form=form, title='Update order')


@app.route("/delete_order/<order_id>", methods=['GET', 'POST'])
def delete_order(order_id):
    order = Orders.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Your order was deleted successfully', 'success')
    return redirect(url_for('index'))


@app.route("/cars", methods=['GET', 'POST'])
def show_cars():
    cars = Cars.query.all()
    return render_template('cars.html', cars=cars)


@app.route("/add_car", methods=['GET', 'POST'])
def add_car():
    form = AddCar()
    car = Cars.query.filter_by(car_number=form.car_number.data).first()
    if form.validate_on_submit() and car is None:
        car = Cars(car_number=form.car_number.data,
                       car_description=form.car_description.data,
                       rental_cost=form.rental_cost.data)
        db.session.add(car)
        db.session.commit()
        flash('Your car was created successful', 'success')
        return redirect(url_for('show_cars'))
    return render_template('add_car.html', form=form)


@app.route("/update_car/<car_id>", methods=['GET', 'POST'])
def update_car(car_id):
    car = Cars.query.filter_by(id=car_id).first()
    form = AddCar()
    if form.validate_on_submit():
        car = Cars(car_number=form.car_number.data,
                   car_description=form.car_description.data,
                   rental_cost=form.rental_cost.data)
        db.session.add(car)
        db.session.commit()
        flash('Your car was updated successful', 'success')
        return redirect(url_for('show_cars'))
    if request.method == 'GET':
        form.car_number.data = car.car_number
        form.car_description.data = car.car_description
        form.rental_cost.data = car.rental_cost
    return render_template('add_car.html', form=form)


@app.route("/delete_car/<car_id>", methods=['GET', 'POST'])
def delete_car(car_id):
    car = Cars.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    flash('Car was deleted successfully', 'success')
    return redirect(url_for('show_cars'))


@app.route("/clients", methods=['GET', 'POST'])
def show_clients():
    clients = Clients.query.all()
    return render_template('clients.html', clients=clients)


@app.route("/add_client", methods=['GET', 'POST'])
def add_client():
    form = AddClient()

    if form.validate_on_submit():
        client = Clients(first_name=form.first_name.data, last_name=form.last_name.data,
                         passport=form.client_passport.data, register_date=form.register_date.data)
        db.session.add(client)
        db.session.commit()
        flash('The client was successfully added', 'success')
        return redirect(url_for('show_clients'))
    return render_template('add_client.html', form=form)


@app.route("/delete_client/<client_id>", methods=['GET', 'POST'])
def delete_client(client_id):
    client = Clients.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client was deleted successfully', 'success')
    return redirect(url_for('show_clients'))
