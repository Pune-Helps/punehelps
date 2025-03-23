from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from sqlalchemy.orm import joinedload

import os
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

DB_USERNAME="admin"
DB_PASSWORD="Pune9^0!"
DB_HOST="ph-db-2.cpukwqkiuiyg.us-east-2.rds.amazonaws.com"
DB_PORT="3306"
DB_NAME="pune_seva"

# SQLite database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_DATABASE_URI'] =  f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# Database model for User

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    birthdate = db.Column(db.Date, nullable=False)
    govt_id_type = db.Column(db.String(50), nullable=False, default="")
    govt_id_number = db.Column(db.String(50), nullable=False, default="")
    

    def get_id(self):
        return str(self.id)
        
    @property
    def is_active(self):
        return True

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Keep old category field for backward compatibility during migration
    category = db.Column(db.String(100), nullable=True)
    # New relationship with Category table
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    other_category = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    urgent = db.Column(db.Boolean, nullable=True, default=False)
    expiry_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('listings', lazy=True))
    category_rel = db.relationship('Category', backref=db.backref('listings', lazy=True))

class ListingView(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    listing_id = db.Column(db.Integer, db.ForeignKey('listing.id'), nullable=False)
    viewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viewed_at = db.Column(db.DateTime, default=datetime.utcnow)
    contact_type = db.Column(db.String(10), nullable=False)  # 'email' or 'phone'

    listing = db.relationship('Listing', backref=db.backref('views', lazy=True))
    viewer = db.relationship('User', backref=db.backref('viewed_listings', lazy=True))

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
        phone_number = request.form.get('phone_number')  # Fixed name to match form
        birthdate = request.form.get('birthdate')
        govt_id_type = request.form.get('govt_id_type')
        govt_id_number = request.form.get('govt_id_number')

        # Ensure no duplicate entries
        existing_user = User.query.filter((User.email == email) | (User.username == username) | (User.govt_id_number == govt_id_number)).first()
        if existing_user:
            flash("Email, username, or Government ID already exists!", "danger")
            return render_template('register.html')

        # Hash the password
        password_hash = generate_password_hash(password)

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            phone_number=phone_number,
            birthdate=datetime.strptime(birthdate, '%Y-%m-%d'),
            govt_id_type=govt_id_type,
            govt_id_number=govt_id_number
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error during registration: {e}', 'danger')

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

@app.route('/landing_page')
@login_required
def homepage():
    with app.app_context():
        # Get all categories for the form dropdown
        categories = Category.query.order_by(Category.name).all()
        
        # Get all active listings
        listings = Listing.query.options(joinedload(Listing.user), joinedload(Listing.category_rel)) \
            .filter(Listing.expiry_date >= datetime.today()) \
            .order_by(Listing.created_at.desc()) \
            .all()

    print(f"DEBUG: Sending {len(listings)} listings to template")  # Debugging
    return render_template('landing.html', listings=listings, categories=categories)


@app.route('/submit_help_request', methods=['POST'])
@login_required
def submit_help_request():
    # Fetch user details from the database
    user_id = current_user.id
    
    # Get form data
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category_id')  # Updated field name to match the form
    other_category = request.form.get('other_category') if category_id and Category.query.get(category_id).name == 'Other' else None
    location = request.form.get('location')
    urgent = True if request.form.get('urgent') else False
    expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date() if request.form.get('expiry_date') else None
    
    # Create new listing
    new_listing = Listing(
        user_id=user_id,
        title=title,
        description=description,
        category_id=category_id,
        other_category=other_category,
        location=location,
        urgent=urgent,
        expiry_date=expiry_date,
        created_at=datetime.utcnow()
    )
    
    # Add to database
    db.session.add(new_listing)
    db.session.commit()
    
    flash('Your help request has been posted!', 'success')
    return redirect(url_for('homepage'))

@app.route('/my-ads')
@login_required
def my_ads():
    # Get all listings for the current user
    user_listings = Listing.query.filter_by(user_id=current_user.id).all()
    
    # For each listing, get view statistics
    listings_data = []
    for listing in user_listings:
        email_views = ListingView.query.filter_by(listing_id=listing.id, contact_type='email').count()
        phone_views = ListingView.query.filter_by(listing_id=listing.id, contact_type='phone').count()
        recent_viewers = (ListingView.query
                         .filter_by(listing_id=listing.id)
                         .order_by(ListingView.viewed_at.desc())
                         .limit(5)
                         .all())
        
        listings_data.append({
            'listing': listing,
            'email_views': email_views,
            'phone_views': phone_views,
            'recent_viewers': recent_viewers
        })
    
    return render_template('my_ads.html', listings_data=listings_data)

@app.route('/delete-listing/<int:listing_id>', methods=['POST'])
@login_required
def delete_listing(listing_id):
    listing = Listing.query.get_or_404(listing_id)
    
    # Check if the current user owns this listing
    if listing.user_id != current_user.id:
        flash('You do not have permission to delete this listing.', 'danger')
        return redirect(url_for('my_ads'))
    
    # Delete associated views first
    ListingView.query.filter_by(listing_id=listing_id).delete()
    
    # Delete the listing
    db.session.delete(listing)
    db.session.commit()
    
    flash('Your listing has been deleted successfully.', 'success')
    return redirect(url_for('my_ads'))

@app.route('/record-view/<int:listing_id>/<contact_type>')
@login_required
def record_view(listing_id, contact_type):
    if contact_type not in ['email', 'phone']:
        return jsonify({'error': 'Invalid contact type'}), 400
        
    # Check if user has already viewed this contact info
    existing_view = ListingView.query.filter_by(
        listing_id=listing_id,
        viewer_id=current_user.id,
        contact_type=contact_type
    ).first()
    
    if not existing_view:
        new_view = ListingView(
            listing_id=listing_id,
            viewer_id=current_user.id,
            contact_type=contact_type
        )
        db.session.add(new_view)
        db.session.commit()
    
    return jsonify({'success': True})

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

    # Check if "Other" is selected, then store other_category
    other_category = request.form.get('other_category') if category == "Other" else None

    flash('Your help request has been submitted!', 'success')
    return redirect(url_for('homepage'))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
