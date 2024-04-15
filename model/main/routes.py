#!/usr/bin/python3
from flask import render_template, redirect, flash, Blueprint, url_for
from model.base import Job, Client, Plumber
from flask_login import current_user, login_required, logout_user, AnonymousUserMixin


main = Blueprint('main', __name__, url_prefix="/", template_folder='templates', static_folder='static')

@main.route("/")
@main.route("/home")
def home():
    """Renders the homepage to everyone"""
    jobs = Job.query.order_by(Job.date_posted.desc()).all()  # Ordering jobs by date_posted descending
    return render_template('home.html', jobs=jobs)



@main.route('/dashboard')
def dashboard():
  if not current_user.is_authenticated or isinstance(current_user, AnonymousUserMixin):
    flash('You are not logged in!', 'danger')
    return redirect(url_for('main.home'))

  if isinstance(current_user, Client):
    # Retrieve jobs for the client (logic to fetch relevant jobs)
    # jobs = Job.query.filter_by(client=current_user).all()
    return render_template('client.html', title='Dashboard')
  elif isinstance(current_user, Plumber):  # Check for plumber type (future use)
    return render_template('plumber.html')

  # Handle unexpected user types (optional)
  else:
    flash('Unexpected user type!', 'warning')
    return redirect(url_for('main.home'))
  # Implement plumber dashboard later
    
    
@main.route('/logout')
@login_required
def logout():
    """remove the username from the session if it's there"""
    logout_user()
    flash(f'You have been logged out!', 'warning')
    return redirect(url_for('main.home')) 


@main.route('/accounts')
def accounts():
    """Checks the instance and routes the user to the account"""
    if isinstance(current_user, Client):

        # return render_template('second_profiles.html', title='Account')
        return redirect(url_for('client_s.account'))
    elif isinstance(current_user, Plumber):  # Check for plumber type (future use)
        # return render_template('second_profile.html')
        return redirect(url_for('plums.accounts'))
    # Handle unexpected user types
    else:
        flash('Unexpected user type!', 'warning')
        return redirect(url_for('main.home'))
    