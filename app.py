from flask import Flask, request, render_template, redirect, url_for
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Pune Seva!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


# Database connection setup (Point 3)
db_connection = pymysql.connect(
    host="ph-db-1.cjkwguo8ka1f.ap-south-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="Pune9^0!",
    db="Punehelps"
)
cursor = db_connection.cursor()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password_hash = request.form['password']  # Assuming password is hashed before submission
        phone_number = request.form['phone']
        birthdate = request.form['birthdate']  # Capturing birthdate from the form

        # SQL Query to insert a new user
        sql = """
        INSERT INTO users (username, email, password_hash, phone_number, birthdate)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (username, email, password_hash, phone_number, birthdate))
            db_connection.commit()
        except pymysql.MySQLError as e:
            print("Error: ", e)
            return "Error during registration"

        return redirect(url_for('login'))  # Redirect to the login page after successful registration

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_or_email = request.form['username']
        password = request.form['password']  # Hash the password before comparing

        # SQL query to fetch user by username or email
        sql = "SELECT * FROM users WHERE (username = %s OR email = %s) AND password_hash = %s"
        cursor.execute(sql, (username_or_email, username_or_email, password))
        user = cursor.fetchone()

        if user:
            # If user exists and password matches
            return "Logged in successfully"
        else:
            # Login failed
            return "Invalid username, email, or password"

    return render_template('login.html')


