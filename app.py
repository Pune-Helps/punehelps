from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Database model for User
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    birthdate = db.Column(db.Date, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    urgent = db.Column(db.Boolean, default=False)
    expiry_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



# Create the tables if they don't exist
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return redirect(url_for('homepage'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone_number = request.form.get('phone')
        birthdate = request.form.get('birthdate')

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        # Create new user
        new_user = User(username=username, email=email, phone_number=phone_number,
                        birthdate=datetime.strptime(birthdate, '%Y-%m-%d'))
        new_user.set_password(password)

        try:
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {e}', 'danger')
            return render_template('register.html')

    return render_template('register.html')


@app.route('/search_listings')
def search_listings():
    search_term = request.args.get('search', '')

    # Query the database for listings that match the search term in title or description
    filtered_listings = Listing.query.filter(
        (Listing.title.ilike(f'%{search_term}%')) | (Listing.description.ilike(f'%{search_term}%'))
    ).all()

    return render_template('landing.html', listings=filtered_listings)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        # Fetch user by username or email
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('homepage'))
        else:
            flash('Invalid username, email, or password', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/lending_page')
@login_required
def homepage():
    # Fetch all active listings from the database (before the expiry date)
    listings = Listing.query.filter(Listing.expiry_date >= datetime.today()).order_by(Listing.created_at.desc()).all()

    return render_template('landing.html', listings=listings)


@app.route('/submit_help_request', methods=['POST'])
@login_required
def submit_help_request():
    # Fetch user details from the database
    user_id = current_user.id

    # Process form data
    title = request.form.get('title')
    description = request.form.get('description')
    category = request.form.get('category')
    location = request.form.get('location')
    urgent = 'urgent' in request.form  # Checkbox value
    expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d')

    # Save to the database
    new_listing = Listing(user_id=user_id, title=title, description=description, category=category,
                          location=location, urgent=urgent, expiry_date=expiry_date)
    db.session.add(new_listing)
    db.session.commit()

    flash('Your help request has been submitted!', 'success')
    return redirect(url_for('homepage'))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
