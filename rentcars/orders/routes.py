from datetime import datetime
from flask import render_template, url_for, redirect, flash, request, Blueprint
from rentcars import db
from rentcars.models import Orders, Cars, Clients
from rentcars.orders.forms import AddOrder


orders = Blueprint('orders', __name__)


@orders.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        start = datetime.strptime(request.form['calendar_start'], "%Y-%m-%d").date()
        end = datetime.strptime(request.form['calendar_end'], "%Y-%m-%d").date()
        orders = Orders.query.filter(Orders.date_rent.between(start, end))
        return render_template('index.html', orders=orders, start=start, end=end)
    start = datetime.strptime('31-12-1970', "%d-%m-%Y").date()
    end = datetime.strptime('31-12-2100', "%d-%m-%Y").date()
    orders = Orders.query.all()
    return render_template('index.html', orders=orders, start=start, end=end)


@orders.route("/add_order", methods=['GET', 'POST'])
def add_order():
    form = AddOrder()
    if form.validate_on_submit():
        print(form.car_number.data.car_number)
        car = Cars.query.filter_by(car_number=form.car_number.data.car_number).first()
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
        client = Clients.query.filter_by(passport=form.client_passport.data.passport).first()
        client.number_orders += 1
        db.session.commit()
        flash('Your order was created successful', 'success')
        return redirect(url_for('orders.index'))
    return render_template('add_order.html', form=form, title='Add order')


@orders.route("/update_order/<order_id>", methods=['GET', 'POST'])
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
        return redirect(url_for('orders.index'))
    if request.method == 'GET':
        form.car_number.data = order.car_number
        form.car_description.data = order.car_description
        form.client_passport.data = order.client_passport
        form.order_date.data = order.date_rent
        form.rental_time.data = order.rental_time

    return render_template('add_order.html', form=form, title='Update order')


@orders.route("/delete_order/<order_id>", methods=['GET', 'POST'])
def delete_order(order_id):
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