from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Create a temporary app instance to update the models
app = Flask(__name__)

DB_USERNAME="admin"
DB_PASSWORD="Pune9^0!"
DB_HOST="ph-db-2.cpukwqkiuiyg.us-east-2.rds.amazonaws.com"
DB_PORT="3306"
DB_NAME="pune_seva"

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Category model
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'

# Update the Listing model to include the relationship with Category
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # Keep the old category field for backward compatibility during migration
    category = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    other_category = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    urgent = db.Column(db.Boolean, nullable=True, default=False)
    expiry_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    
    # Define the relationship with Category
    category_rel = db.relationship('Category', backref=db.backref('listings', lazy=True))
    
    def __repr__(self):
        return f'<Listing {self.title}>'

# Create the tables if they don't exist
with app.app_context():
    db.create_all()
    print("Models updated successfully!")

print("Run the SQL migration script to migrate existing data.")
