from app import app
from flask import render_template, url_for, redirect, flash
from models import Orders, Cars
from app import db
from forms import AddOrder


@app.route('/')
def index():
    orders = Orders.query.all()

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
    cars = Cars.query.all()
    return render_template('index.html', cars=cars)