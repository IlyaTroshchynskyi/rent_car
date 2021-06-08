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
        # car_number = db.Column(db.String(10), unique=True)
        # client_passport = db.Column(db.String(10), unique=True)
        # date_rent = db.Column(db.DateTime, nullable=False, default=datetime.now())
        # rental_time = db.Column(db.Integer, nullable=False)
        # rental_cost = db.Column(db.Float)
        # total_cost = db.Column(db.Float)
        # car = db.relations
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
