import os
from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from forms import Registration_Form, Login_Form
from flask_login import LoginManager, login_user, current_user, login_required
from functions import valid_login
from model.base import Client, Plumber
from model.engine.file_storage import DataStorage as store_data
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# Initialize Flask-Login with your app
login_manager = LoginManager()
login_manager.init_app(app)


app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Base = db.Model
migrate = Migrate(app, db)
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


@app.route("/login", methods=['GET', 'POST'])
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

@app.route('/client')
@login_required
def client_view():
    """ A function that renders the home page """
    return render_template('login.html', title='client')


@app.route("/dashboard")
@login_required  # Require login for this route
def dashboard():
    """Renders the dashboard only for authenticated users."""
    # Display dashboard content for logged-in user
    return render_template('client.html')

@app.route('/profile/update', methods=['POST'])
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
   



if __name__ == '__main__':
    app.run(debug=True)