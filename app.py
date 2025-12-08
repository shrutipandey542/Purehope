from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# MySQL Configuration
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your actual username
            password='WJ28@krhps',  # Replace with your actual password
            database='sql'
        )
        if conn.is_connected():
            print("Connected to MySQL successfully!")
            return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    return None

@app.route('/test_db')
def test_db():
    connection = get_db_connection()
    if connection:
        return "Database connected successfully!"
    else:
        return "Failed to connect to the database."

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('fullName')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmPassword')

        if not (full_name and email and password and confirm_password):
            flash('All fields are required!', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM signup WHERE Email_Address = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Email already registered! Please use a different email.', 'error')
                return redirect(url_for('signup'))

            # Insert data
            query = "INSERT INTO signup (Full_Name, Email_Address, Password, Confirm_Password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (full_name, email, password, confirm_password))
            connection.commit()

            cursor.execute("INSERT INTO login (email_address, password) VALUES (%s, %s)", (email, password))
            connection.commit()

            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))

        except mysql.connector.IntegrityError as err:
            if err.errno == 1062:  # Handle duplicate entry error
                flash('Email already registered! Please use a different email.', 'error')
            else:
                flash(f'Database Error: {err}', 'error')
            return redirect(url_for('signup'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
            return redirect(url_for('signup'))
        finally:
            cursor.close()
            connection.close()

    return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            connection = get_db_connection()
            if not connection:
                flash('Failed to connect to the database.', 'error')
                return redirect(url_for('login'))

            cursor = connection.cursor()
            query = "SELECT * FROM signup WHERE Email_Address=%s AND Password=%s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()

            if user:
                flash('Login successful!', 'success')
                return redirect(url_for('donate'))
            else:
                flash('Invalid email or password.', 'error')
                return redirect(url_for('login'))

        except Exception as e:
            flash(f'Error: {e}', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/donate')
def donate():
    return render_template('donate.html')
# ----------------------------
# ADD API ROUTES BELOW THIS
# ----------------------------

@app.route('/api/users', methods=['GET'])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT Full_Name, Email_Address FROM signup")
    users = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(users)


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM signup WHERE Email_Address=%s AND Password=%s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    connection.close()

    if user:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "error", "message": "Invalid credentials"})

if __name__ == '__main__':
    app.run(debug=True)