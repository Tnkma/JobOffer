from model import app, Base, bcrypt, login_manager
from model.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostJobForm
from flask_login import current_user, login_required, login_user, logout_user
from flask import render_template, url_for, flash, redirect, request, session
from model.base import Client, Plumber, Job
from model.func import *


@login_manager.user_loader
def load_user(user_id):
    # Assuming Client objects have a primary key 'id'
    return get_single(Client, id=user_id)


@app.route("/jobs")
@app.route("/home")
def home():
    """ Renders the homepage to everyone """
    jobs=Job.query.all()
    return render_template('home.html', jobs=jobs)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register a new client """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        client = Client(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data, state=form.state.data)
        new(client)
        save()
        flash(f'Account created, You can now login', 'success')
        return redirect(url_for('login'))
    
    # flash(f'Account not created, Please fill the forms correctly!', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    """We create a object of the Login_Form class"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Client.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')    
    return render_template('login.html', title='Login', form=form)



@app.route('/plumber', methods=['GET', 'POST'], strict_slashes=False)
@login_required  # Ensure user is logged in before accessing the dashboard
def plumber_dashboard():
    """Renders the plumber dashboard template with a descriptive title."""
    title = "Plumber Dashboard"  # Set a more appropriate title
    return render_template('plumber.html', title=title)

@app.route("/dashboard", strict_slashes=False) 
# Require login for this route
def dashboard():
    """Renders the dashboard only for authenticated users."""
    if current_user.is_authenticated:
        return render_template('client.html')
    flash(f'Please login to access the dashboard', 'danger')
    return redirect(url_for('login'))

@app.route('/profile/update', methods=['POST'], strict_slashes=False)
def update_profile():
    service_areas = request.form.get('service_areas')
    bio = request.form.get('bio')
    # Get the current logged-in client using session to update profile
    current_client = current_user()
    current_client.service_areas = service_areas
    current_client.bio = bio
    save()
    # return 'Profile updated successfully!'
    flash('Profile updated successfully!', 'success')
 
    
@app.route('/logout')
def logout():
    """remove the username from the session if it's there"""
    logout_user()
    flash(f'You have been logged out!', 'warning')
    return redirect(url_for('home'))


@app.route("/account", methods=['GET','POST'], strict_slashes=False)
def account():
    """ Update the account """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.state.data = current_user.state
    return render_template('profile.html', title='Account', form=form)

@app.route("/jobs/new", methods=['GET', 'POST'], strict_slashes=False)
@login_required
def post_new_job():
    """ Posts new job"""
    form = PostJobForm()
    if form.validate_on_submit():
        job  = Job(job_title=form.job_title.data, content=form.content.data, location=form.state.data, job_description=form.job_description.data, posted_by_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        flash(f'Job posted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('post_job.html', title='Post Job', form=form)
        
    