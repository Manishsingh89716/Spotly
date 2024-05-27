# import all required libraries

from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# secret key for session management
app.secret_key = 'your_secret_key'

# database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='spotly'
    )
    return conn

# route for the home page
@app.route('/')
def index():
    return render_template('home.html')

# route for the user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        conn.commit()
        cursor.close()
        conn.close()
        return 'Registration successful! Please <a href="/login">login</a>.'
    return render_template('register.html')

# route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

# route for home page after login
@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# route page for making reservation
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        train_number = request.form['train_number']
        train_name = request.form['train_name']
        class_type = request.form['class_type']
        date_of_journey = request.form['date_of_journey']
        from_place = request.form['from_place']
        to_place = request.form['to_place']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO reserve (user_id, train_number, train_name, class_type, date_of_journey, from_place, to_place) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (session['user_id'], train_number, train_name, class_type, date_of_journey, from_place, to_place))
        conn.commit()
        cursor.close()
        conn.close()
        return 'Reservation successful!'
    return render_template('reservation.html')

# route page for cancelling a reservation
@app.route('/cancellation', methods=['GET', 'POST'])
def cancellation():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        pnr = request.form['pnr']
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM reserve WHERE id = %s AND user_id = %s', (pnr, session['user_id']))
        reservation = cursor.fetchone()
        if reservation:
            cursor.execute('DELETE FROM reserve WHERE id = %s', (pnr,))
            conn.commit()
            cursor.close()
            conn.close()
            return 'Cancellation successful!'
        else:
            cursor.close()
            conn.close()
            return 'Invalid PNR number or unauthorized access'
    return render_template('cancellation.html')

# route page for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
