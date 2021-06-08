from app import app
from flask import render_template, url_for
from models import Orders, Cars
from app import db
from forms import AddOrder


@app.route('/')
def index():
    orders = Orders.query.all()

    return render_template('index.html', orders=orders)


@app.route('/add_order')
def add_order():
    form = AddOrder()
    return render_template('add_order.html', form=form)