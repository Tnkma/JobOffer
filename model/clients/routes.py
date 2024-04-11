#!/usr/bin/python3

from model import app, bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import current_user, login_user, login_required
from flask import render_template, flash, redirect, request, Blueprint, url_for, abort
from model.base import Client, Job, JobPlumber, Plumber
from .utils import *

client_s = Blueprint('client_s', __name__, url_prefix="/clients", template_folder='templates', static_folder='static')




@login_manager.user_loader
def load_user(user_id):
    # Assuming Client objects have a primary key 'id'
    #return get_single(Client, id=user_id)
    client = Client.query.get(int(user_id))
    return client



@client_s.route("/register", methods=['GET', 'POST'])
def registers():
    """ Register a new client """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        client = Client(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data, state=form.state.data)
        new(client)
        save()
        flash(f'Account created, You can now login', 'success')
        return redirect(url_for('client_s.login'))
    # flash(f'Account not created, Please fill the forms correctly!', 'danger')
    return render_template('registers.html', title='Register', form=form)


@client_s.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    """We create a object of the Login_Form class"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Client.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')    
    return render_template('login_client.html', title='Login', form=form)


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
        return redirect(url_for('client_s.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.state.data = current_user.state
    return render_template('second_profile.html', title='Account', form=form)


# takes the user to client_dasboard
@client_s.route("/dashboard", strict_slashes=False)
@login_required
def dashboard():
    """Renders the dashboard only for authenticated users."""
    return render_template('client.html')

# Jobs the current_user posted
@client_s.route("/dashboard/posted_jobs",  methods=['GET','POST'],strict_slashes=False)
def posted_jobs():
    """ Renders the jobs posted by the client """
    jobs = Job.query.filter_by(client_id=current_user.id).all()
    return render_template('posted_jobs.html', jobs=jobs)


# view applicants and assigned jobs
@client_s.route("/jobs/<int:job_id>/applicants", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def view_applicants(job_id):    
    """ View the list of plumbers who applied for a particular job """
    job = Job.query.get_or_404(job_id)
    # Ensure the job belongs to the current client (authorization check)
    if job.client != current_user:
        abort(403)  # Forbidden access if not the client's job
    # Retrieve plumbers who applied
    applicants = (
        db.session.query(Plumber)
        .join(JobPlumber, JobPlumber.plumber_id == Plumber.id)
        .filter(JobPlumber.job_id == job_id)
        .all()
    )
    # Handle form submission
    if request.method == 'POST':
        selected_plumber_id = request.form.get('assigned_plumber')
        if selected_plumber_id:
            try:
                selected_plumber = Plumber.query.get(int(selected_plumber_id))
                if selected_plumber:
                    # Check if an existing entry exists (optional)
                    existing_assignment = JobPlumber.query.filter_by(job=job, plumber=selected_plumber).first()
                    if existing_assignment:
                        existing_assignment.is_assigned = True
                        flash('Job assigned already', 'warning')
                    else:
                        # Create a new entry if it doesn't exist
                        new_assignment = JobPlumber(job=job, plumber=selected_plumber, is_assigned=True)
                        new(new_assignment)
                        save()
                        flash('Job successfully assigned!', 'success')
                        return redirect(url_for('client_s.view_jobs'))  # Redirect after successful assignment
                else:
                    flash('Invalid plumber selection!', 'error')
            except ValueError:  # Handle potential conversion errors
                flash('Invalid selection!', 'error')
    return render_template('applicants.html', title='Job Applicants', job=job, applicants=applicants)
            
        
