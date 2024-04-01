from model import app
from model.forms import Registration_Form, Login_Form, valid_login
from flask_login import current_user, login_required
from flask import render_template, url_for, flash, redirect, request, session
from model.base import Client, Plumber
from flask_login import LoginManager
from model.engine.file_storage import DataStorage as store_data



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


@app.route("/")
@app.route("/home")
def home():
    """ Renders the homepage to everyone """
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Register a new client """
    form = Registration_Form(request.form)
    if form.validate_on_submit():
        user = Client(username=form.username.data, email=form.email.data, phone_no=form.phone.data, state=form.state.data)
        store_data.add_new(user)
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    flash(f'Account not created, Please fill the forms correctly!', 'danger')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'], STRICT_SLASHES=False)
def login():
    """We create a object of the Login_Form class"""
    form = Login_Form()
    if form.validate_on_submit():
        if valid_login(form.email.data, form.password.data):
            session['username'] = request.form['username']
            flash('You have been logged in!', 'success')
            return redirect(url_for('client_view'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')    
    return render_template('login.html', title='Login', form=form)

@app.route("/plumber")
def plumber_dashboard():
    return render_template('plumber.html', title='register')

@app.route('/client', methods=['GET', 'POST'], STRICT_SLASHES=False)
@login_required
def client_view():
    """ A function that renders the home page """
    return render_template('login.html', title='client')


@app.route("/dashboard", STRICT_SLASHES=False)
@login_required  # Require login for this route
def dashboard():
    """Renders the dashboard only for authenticated users."""
    # Display dashboard content for logged-in user
    return render_template('client.html')

@app.route('/profile/update', methods=['POST'], STRICT_SLASHES=False)
def update_profile():
    service_areas = request.form.get('service_areas')
    bio = request.form.get('bio')
    # Get the current logged-in client using session to update profile
    current_client = current_user()
    current_client.service_areas = service_areas
    current_client.bio = bio
    store_data.db_commit()
    # return 'Profile updated successfully!'
    flash('Profile updated successfully!', 'success')
 
    
@app.route('/logout')
def logout():
    """remove the username from the session if it's there"""
    session.pop('username', None)
    return redirect(url_for('/home'))
   

