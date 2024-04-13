#!/usr/bin/python3

from model import app, bcrypt, login_manager
from .forms import RegistrationForm, LoginForm, UpdateAccountForm, SelectState
from flask_login import current_user, login_user, login_required
from flask import render_template, flash, redirect, request, Blueprint, url_for
from model.base import Client, Job, JobPlumber, Plumber
from .utils import *

client_s = Blueprint(
    'client_s',
    __name__, 
    url_prefix="/clients",
    template_folder='templates',
    static_folder='static'
)

@login_manager.user_loader
def load_user(user_id):
    """ load the user """
    try:
        client = Client.query.get(user_id)
        return client
    except:
        return None



@client_s.route("/register", methods=['GET', 'POST'])
def registers():
    """ Register a new client """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        client = Client(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            phone=form.phone.data,
            state=form.state.data
        )
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

# Jobs the current_user posted
@client_s.route("/dashboard/posted_jobs",  methods=['GET','POST'],strict_slashes=False)
def posted_jobs():
    """ Renders the jobs posted by the client """
    jobs = Job.query.filter_by(client_id=current_user.id).all()
    return render_template('posted_jobs.html', jobs=jobs)


@client_s.route("/dashboard/applicants", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def view_applicants():
    """ View the list of applicants and assign plumbers for all of the current client's jobs """

    # Get all jobs posted by the current client
    current_user_jobs = Job.query.filter_by(client_id=current_user.id).all()

    # Prepare a dictionary to store applicants for each job
    job_applicants = {}
    for job in current_user_jobs:
        applicants = (
            db.session.query(Plumber)
            .join(JobPlumber, JobPlumber.plumber_id == Plumber.id)
            .filter(JobPlumber.job_id == job.id)
            .all()
        )
        job_applicants[job.id] = applicants

    # Handle form submission for assigning a plumber
    if request.method == 'POST':
        selected_job_id = request.form.get('job_id')
        selected_plumber_id = request.form.get('assigned_plumber')

        if selected_job_id and selected_plumber_id:
            try:
                selected_job = Job.query.get(int(selected_job_id))
                selected_plumber = Plumber.query.get(int(selected_plumber_id))

                if selected_job and selected_plumber and selected_job.client == current_user:
                    # Check if an existing assignment exists for this job and plumber
                    existing_assignment = JobPlumber.query.filter_by(job=selected_job, plumber=selected_plumber).first()
                    if existing_assignment:
                        existing_assignment.is_assigned = True
                        flash('Job assigned already.', 'warning')
                    else:
                        # Create a new assignment if it doesn't exist
                        new_assignment = JobPlumber(job=selected_job, plumber=selected_plumber, is_assigned=True)
                        new(new_assignment)
                        save()
                        flash('Job successfully assigned!', 'success')
                    #return redirect(url_for('client_s.view_applicants'))  # Refresh after assignment
                else:
                    flash('Invalid job or plumber selection.', 'error')
            except ValueError:
                flash('Invalid selection!', 'error')

    return render_template(
        'applicant.html',
        title='View Applicants',
        job_applicants=job_applicants,
        current_user_jobs=current_user_jobs
    
    )
    
    
    
@client_s.route("/dashboard/get_plumber_by_state", methods=['GET', 'POST'])
def get_state():
  """gets plumbers based on sate"""
  form = SelectState()

  if form.validate_on_submit():
    states = form.state.data
    plumber = Plumber.query.filter_by(state=states).all()
    return render_template('get_plum.html', form=form, plumber=plumber)  # Pass form for error display
  else:
    return render_template('get_plum.html', form=form)  # Pass form for error display




@client_s.route("/assigned_plumber", methods=['POST', 'GET'])
def assigned_plumber():
    """Gets the plumbers assigned to jobs"""
    posted_jobs = Job.query.filter_by(client_id=current_user.id).all()
    assigned_plumbers = {}
    for job in posted_jobs:
        plumbers = (
            db.session.query(Plumber)
            .join(JobPlumber, JobPlumber.plumber_id == Plumber.id)
            .filter(JobPlumber.job_id == job.id, JobPlumber.is_assigned == True)
            .all()
        )
        assigned_plumbers[job] = plumbers

    # Print the contents of assigned_plumbers for debugging
    return render_template('assigned_jobs.html', title='Assigned Plumbers', assigned_plumbers=assigned_plumbers)

