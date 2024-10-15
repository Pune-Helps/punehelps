from flask import Flask, request, render_template, redirect, url_for, flash
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Database connection setup function
def get_db_connection():
    return pymysql.connect(
        host="ph-db-1.cjkwguo8ka1f.ap-south-1.rds.amazonaws.com",
        port=3306,
        user="admin",
        password="Pune9^0!",
        db="Punehelps"
    )

#@app.route('/')
#def home():
#    return "Welcome to Pune Seva!"

@app.route('/')
def homepage():
    with db.cursor() as cursor:
        query = """
        SELECT id, title, description, category, location, image
        FROM listings
        WHERE expiry_date > NOW()
        ORDER BY created_at DESC
        """
        cursor.execute(query)
        listings = cursor.fetchall()
    return render_template('landing.html', listings=listings)

@app.route('/search_listings')
def search_listings():
    search_term = request.args.get('search', '')
    with db.cursor() as cursor:
        query = """
        SELECT id, title, description, category, location, image
        FROM listings
        WHERE title LIKE %s OR description LIKE %s
        """
        cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))
        listings = cursor.fetchall()
    return render_template('landing.html', listings=listings)

# Other routes (login, register) go here...

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Get the raw password
        phone_number = request.form['phone']
        birthdate = request.form['birthdate']

        # Hash the password before storing it
        password_hash = generate_password_hash(password)

        # SQL query to insert a new user
        sql = """
        INSERT INTO users (username, email, password_hash, phone_number, birthdate)
        VALUES (%s, %s, %s, %s, %s)
        """

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (username, email, password_hash, phone_number, birthdate))
            connection.commit()
            cursor.close()
            connection.close()

            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except pymysql.MySQLError as e:
            flash(f'Error during registration: {e}', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']

        # SQL query to fetch user by username or email
        sql = "SELECT * FROM users WHERE username = %s OR email = %s"

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(sql, (username_or_email, username_or_email))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user and check_password_hash(user[3], password):  # Assuming password_hash is in the 4th column
                flash('Login successful!', 'success')
                # Here you can set session data or redirect to the home/dashboard page
                return redirect(url_for('home'))
            else:
                flash('Invalid username, email, or password', 'danger')

        except pymysql.MySQLError as e:
            flash(f'Error during login: {e}', 'danger')

    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)