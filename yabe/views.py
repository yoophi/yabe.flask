from flask import Flask, request, render_template, redirect, url_for, abort, jsonify, session
from flask.ext.login import LoginManager, login_user, logout_user
from form import AppointmentForm, LoginForm

from . import app, db
from .models import Appointment, User


@app.route('/appointments/create/', methods=['GET', 'POST'])
def appointment_create():
    form = AppointmentForm(request.form)
    app.logger.debug(form)
    if request.method == 'POST' and form.validate():
        appt = Appointment()
        form.populate_obj(appt)
        db.session.add(appt)
        db.session.commit()
        return redirect(url_for('appointment_list'))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/')
def appointment_list():
    app.logger.debug(session)
    appts = Appointment.query.order_by(Appointment.start.asc()).all()
    return render_template('appointment/index.html', appts=appts)


@app.route('/appointments/<int:appointment_id>/')
def appointment_detail(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if appt is None:
        abort(404)
    return render_template('appointment/detail.html', appt=appt)


@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
def appointment_edit(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if appt is None:
        abort(404)
    form = AppointmentForm(request.form, appt)
    if request.method == 'POST' and form.validate():
        form.populate_obj(appt)
        db.session.commit()
        return redirect(url_for('appointment_detail', appointment_id=appt.id))
    return render_template('appointment/edit.html', form=form)


@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
def appointment_delete(appointment_id):
    appt = Appointment.query.get(appointment_id)
    if appt is None:
        response = jsonify({'status': 'Not Found'})
        response.status_code = 404
        return response
    db.session.delete(appt)
    db.session.commit()
    return jsonify({'status': 'OK'})


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    app.logger.debug(request.form)
    error = None
    if request.method == 'POST' and form.validate():
        email = form.username.data.lower().strip()
        password = form.password.data.lower().strip()
        user, authenticated = User.authenticate(db.session.query, email, password)
        if authenticated:
            login_user(user)
            return redirect(url_for('appointment_list'))
        else:
            error = 'Incorrect username or password. Try again.'
    return render_template('user/login.html', form=form, error=error)


@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))



