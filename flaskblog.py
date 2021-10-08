# TODO: add in commit validation to git (black, pylava)
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from typing import Callable

# Flask application configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf44d8000ecb0f94f01dcc7451318648' # TODO: Add to .secrets dir
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/site.db'


class MySQLAlchemy(SQLAlchemy):
    # Workaround for issues with IDE not recognising Flask SQLAlchemy methods: https://www.py4u.net/discuss/167613
    Column: Callable
    String: Callable
    Integer: Callable
    relationship: Callable
    Text: Callable
    DateTime: Callable
    ForeignKey: Callable


db = MySQLAlchemy(app)  # SQLAlchemy database instance created


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # Uppercase Post refers to class

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Lowercase user refers to table name

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}'"

posts = [
    {
        'author': 'Matt Hill',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': '2021-09-01'
    },
    {
        'author': 'Matt Hill',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': '2021-09-02'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm() # Instance of registration form
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()  # Instance of registration form
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'Successful login for email {form.email.data}', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
