#!/usr/bin/python3

from model import app, bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import current_user, login_user
from flask import render_template, flash, redirect, request, Blueprint
from model.base import Client
from .utils import *

client_s = Blueprint('client_s', __name__)




@login_manager.user_loader
def load_user(user_id):
    # Assuming Client objects have a primary key 'id'
    #return get_single(Client, id=user_id)
    client = Client.query.get(int(user_id))
    return client



@client_s.route("/register", methods=['GET', 'POST'])
def register():
    """ Register a new client """
    if current_user.is_authenticated:
        return redirect(client_s.url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        client = Client(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data, state=form.state.data)
        new(client)
        save()
        flash(f'Account created, You can now login', 'success')
        return redirect(client_s.url_for('login'))
    
    # flash(f'Account not created, Please fill the forms correctly!', 'danger')
    return render_template('register.html', title='Register', form=form)


@client_s.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    """We create a object of the Login_Form class"""
    if current_user.is_authenticated:
        return redirect(client_s.url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Client.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
            return redirect(client_s.url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')    
    return render_template('login.html', title='Login', form=form)


@client_s.route("/account", methods=['GET','POST'], strict_slashes=False)
def account():
    """ Update the account """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        save()
        flash('Your account has been updated!', 'success')
        return redirect(client_s.url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.state.data = current_user.state
    return render_template('second_profile.html', title='Account', form=form)


@client_s.route("/dashboard", strict_slashes=False) 
def dashboard():
    """Renders the dashboard only for authenticated users."""
    if current_user.is_authenticated:
        return render_template('client.html')
    flash(f'Please login to access the dashboard', 'danger')
    return redirect(client_s.url_for('login'))
