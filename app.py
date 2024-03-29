import os
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from functions import valid_login

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
    return render_template('home.html', posts=posts)


@app.route("/profile")
def about():
    return render_template('profile.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # We create a object of the LoginForm class
    form = LoginForm()
    if form.validate_on_submit():
        if valid_login(form.email.data, form.password.data):
            flash('You have been logged in!', 'success')
            return redirect(url_for('plumber_dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')    
    return render_template('login.html', title='Login', form=form)

@app.route("/plumber")
def plumber_dashboard():
    return render_template('plumber.html', title='register')

@app.route('/client')
def client_view():
    return render_template('client.html', title='client')


if __name__ == '__main__':
    app.run(debug=True)