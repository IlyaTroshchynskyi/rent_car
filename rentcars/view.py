from app import app
from flask import render_template, url_for, redirect, flash, request
from models import Orders, Cars
from app import db
from forms import AddOrder, AddCar


@app.route('/')
def index():
    # orders = Orders.query.all()
    orders = []
    return render_template('index.html', orders=orders)


@app.route("/add_order", methods=['GET', 'POST'])
def add_order():
    form = AddOrder()
    print('**************')
    if form.validate_on_submit():
        print('////////////')
        car = Cars.query.filter_by(car_number=form.car_number.data).first()
        order = Orders(car_number=form.car_number.data,
                       client_passport=form.client_passport.data,
                       date_rent=form.order_date.data,
                       rental_time=form.rental_time.data,
                       rental_cost=car.rental_cost,
                       total_cost=form.rental_time.data * car.rental_cost)
        db.session.add(order)
        db.session.commit()
        print(order)
        flash('Your order was created successful', 'success')
        return redirect(url_for('index'))
    return render_template('add_order.html', form=form)


@app.route("/delete/<id_order>", methods=['GET', 'POST'])
def delete_order(id_order):
    order = Orders.query.get_or_404(id_order)
    db.session.delete(order)
    db.session.commit()
    flash('Your order was deleted successfully', 'success')
    return redirect(url_for('index'))


@app.route("/cars", methods=['GET', 'POST'])
def show_cars():
    # cars = Cars.query.all()
    cars = []
    return render_template('cars.html', cars=cars)


@app.route("/add_car", methods=['GET', 'POST'])
def add_car():
    form = AddCar()
    print('**************')
    if form.validate_on_submit():
        print('////////////')
        car = Cars.query.filter_by(car_number=form.car_number.data).first()
        car = Cars(car_number=form.car_number.data,
                       car_descripion=form.car_description.data,
                       rental_cost=form.rental_cost.data,
                       count_orders=form.count_orders.data)
        db.session.add(car)
        db.session.commit()
        flash('Your car was created successful', 'success')
        return redirect(url_for('index'))
    return render_template('add_car.html', form=form)


@app.route("/update_order/<order_id>", methods=['GET', 'POST'])
def update_order(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    form = AddOrder()
    if request.method == 'GET':
        form.car_number.data = order.car_number
        # form.car_description.data = order.car_description
        form.client_passport.data = order.client_passport
        form.client_name.data = order.client_name
        form.date_rent.data = order.date_rent
        form.rental_time.data = order.rental_time

    return render_template('add_order.html', form=form)


@app.route("/clients", methods=['GET', 'POST'])
def show_clients():
    clients = []
    return render_template('clients.html', clients=clients)