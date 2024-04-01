from model import app, Base, bcrypt
from model.forms import RegistrationForm, LoginForm
from flask_login import current_user, login_required, login_user
from flask import render_template, url_for, flash, redirect, request, session
from model.base import Client, Plumber
from flask_login import LoginManager
from model.func import *



# Initialize Flask-Login with your app
login_manager = LoginManager()
login_manager.init_app(app)


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]




@login_manager.user_loader
def load_user(user_id):
    # Assuming Client objects have a primary key 'id'
    return get_single(Client, id=user_id)


@app.route("/")
@app.route("/home")
def home():
    """ Renders the homepage to everyone """
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register a new client """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        client = Client(username=form.username.data, email=form.email.data, password=hashed_password, phone=form.phone.data, state=form.state.data)
        new(client)
        save()
        flash(f'Account created, You can now login', 'success')
        return redirect(url_for('login'))
    flash(f'Account not created, Please fill the forms correctly!', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'], strict_slashes=False)
def login():
    """We create a object of the Login_Form class"""
    form = LoginForm()
    if form.validate_on_submit():
        
        flash('You have been logged in!', 'success')
        return redirect(url_for('client_view'))
    else:
        flash('Login Unsuccessful. Please check username and password', 'danger')    
    return render_template('login.html', title='Login', form=form)



@app.route('/plumber', methods=['GET', 'POST'], strict_slashes=False)
@login_required  # Ensure user is logged in before accessing the dashboard
def plumber_dashboard():
    """Renders the plumber dashboard template with a descriptive title."""
    title = "Plumber Dashboard"  # Set a more appropriate title
    return render_template('plumber.html', title=title)


@app.route('/client', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def client_view():
    """ A function that renders the home page """
    return render_template('login.html', title='client')


@app.route("/dashboard", strict_slashes=False)
@login_required  # Require login for this route
def dashboard():
    """Renders the dashboard only for authenticated users."""
    # Display dashboard content for logged-in user
    return render_template('client.html')

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
    session.pop('username', None)
    return redirect(url_for('/home'))
   

