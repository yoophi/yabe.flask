from flask import Flask, request, render_template, redirect, url_for, abort, jsonify, session
from flask.ext.login import LoginManager, login_user, logout_user
from flask.ext.sqlalchemy import SQLAlchemy
from form import AppointmentForm, LoginForm

# from models import db, Appointment, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db'
app.config['SECRET_KEY'] = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from . import models, views

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


