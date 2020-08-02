import functools
from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_functions import insert_user, get_user

def is_loggedin():
    user_id = session.get('user_id')
    user = get_user(user_id=user_id)
    return user is not None

def logged_in(f):
    """
    Example decorator that checks if the current session is logged in
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if is_loggedin():
            return f(*args, **kwargs)
        return redirect(url_for('signin'))
    return wrapper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DEMONSTRATION_KEY'
app.add_template_global(is_loggedin)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@logged_in
def dashboard():
    return render_template('dashboard.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = get_user(username)
            # Check that this username is not taken
            if not user:
                # Hash the password when inserting a new user
                insert_user(username, generate_password_hash(password))
                flash('Signup successful, please signin now.')
                return redirect(url_for('signin'))
            flash('Username is taken')
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user(username)
        # Check that a user matching the username exists, and that the password matches
        if user is not None and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('signin.html')

@app.route('/signout', methods=['POST'])
@logged_in
def signout():
    session.clear()
    return redirect(url_for('signin'))
