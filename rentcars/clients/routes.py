from datetime import datetime
from flask import render_template, url_for, redirect, flash, request, Blueprint
from rentcars import db
from rentcars.models import Clients
from rentcars.clients.forms import AddClient


clients = Blueprint('clients', __name__)


@clients.route("/clients", methods=['GET', 'POST'])
def show_clients():
    if request.method == 'POST':
        start = datetime.strptime(request.form['calendar_start'], "%Y-%m-%d").date()
        end = datetime.strptime(request.form['calendar_end'], "%Y-%m-%d").date()
        clients = Clients.query.filter(Clients.register_date.between(start, end))
        return render_template('clients.html', clients=clients, start=start, end=end)
    start = datetime.strptime('31-12-1970', "%d-%m-%Y").date()
    end = datetime.strptime('31-12-2100', "%d-%m-%Y").date()
    clients = Clients.query.all()
    return render_template('clients.html', clients=clients, start=start, end=end)


@clients.route("/add_client", methods=['GET', 'POST'])
def add_client():
    form = AddClient()
    if form.validate_on_submit():
        client = Clients(first_name=form.first_name.data, last_name=form.last_name.data,
                         passport=form.client_passport.data, register_date=form.register_date.data)
        db.session.add(client)
        db.session.commit()
        flash('The client was successfully added', 'success')
        return redirect(url_for('clients.show_clients'))
    return render_template('add_client.html', form=form, title='Add client')


@clients.route("/update_client/<client_id>", methods=['GET', 'POST'])
def update_client(client_id):
    client = Clients.query.filter_by(id=client_id).first()
    form = AddClient()
    if form.validate_on_submit():
        client.first_name = form.first_name.data
        client.last_name = form.last_name.data
        client.passport = form.client_passport.data
        client.register_date = form.register_date.data
        db.session.commit()
        flash('The client was successfully updated', 'success')
        return redirect(url_for('clients.show_clients'))
    if request.method == 'GET':
        form.first_name.data = client.first_name
        form.last_name.data = client.last_name
        form.client_passport.data = client.passport
        form.register_date.data = client.register_date
    return render_template('add_client.html', form=form, title='Update client')


@clients.route("/delete_client/<client_id>", methods=['GET', 'POST'])
def delete_client(client_id):
    client = Clients.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    flash('Client was deleted successfully', 'success')
    return redirect(url_for('clients.show_clients'))