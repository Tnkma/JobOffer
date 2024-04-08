#!/usr/bin/python3

from model import bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, request, Blueprint, url_for
from model.base import Plumber
from .utils import *

plums = Blueprint('plums', __name__, url_prefix="/plumber", template_folder='templates', static_folder='static')

@login_manager.user_loader
def load_user(user_id):
    # Assuming Client objects have a primary key 'id'
    #return get_single(Client, id=user_id)
    plumber = Plumber.query.get(int(user_id))
    return plumber


@plums.route("/register", methods=['GET', 'POST'])
def register():
    """ Register a new client """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = Plumber.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('plums.register'))
        
        # Proceed with user registration
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        client = Plumber(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data, state=form.state.data)
        new(client)
        save()
        flash('Account created. You can now login.', 'success')
        return redirect(url_for('plums.login'))

    return render_template('register.html', title='Register', form=form)



@plums.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    """We create a object of the Login_Form class"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Plumber.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')    
    return render_template('login.html', title='Login', form=form)


@plums.route("/dashboard", strict_slashes=False) 
def dashboard():
    """Renders the dashboard only for authenticated users."""
    if current_user.is_authenticated:
        return render_template('plumber.html')
    flash(f'Please login to access the dashboard', 'danger')
    return redirect(url_for('plums.login'))


@plums.route("/account", methods=['GET','POST'], strict_slashes=False)
def account():
    """ Update the account """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('plums.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.state.data = current_user.state
    return render_template('second_profile.html', title='Account', form=form)

