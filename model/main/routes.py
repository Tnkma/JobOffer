#!/usr/bin/python3
from flask import render_template, redirect, flash, Blueprint, url_for
from flask_login import logout_user
from model.base import Job


main = Blueprint('main', __name__, url_prefix="/", template_folder='templates', static_folder='static')

@main.route("/")
@main.route("/home")
def home():
    """ Renders the homepage to everyone """
    jobs = Job.query.all()
    return render_template('home.html', jobs=jobs)

@main.route('/logout')
def logout():
    """remove the username from the session if it's there"""
    logout_user()
    flash(f'You have been logged out!', 'warning')
    return redirect(url_for('main.home'))
