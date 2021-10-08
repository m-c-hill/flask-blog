from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'bf44d8000ecb0f94f01dcc7451318648' # TODO: Add to .secrets dir

# TODO: add in commit validation to git (black, pylava)

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
