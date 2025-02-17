from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Secret key for session management and flash messages
app.secret_key = 'your_secret_key_here'

# In-memory storage for demonstration purposes (consider using a database)
users = []

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get data from form
        full_name = request.form['fullName']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']

        # Validate the input (simple checks)
        if not full_name or not email or not password or not confirm_password:
            flash('All fields are required!', 'error')
            return redirect(url_for('signup'))

        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('signup'))

        # Save the new user (this is just a mockup, use a database in real apps)
        users.append({'full_name': full_name, 'email': email, 'password': password})

        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')  # Create a simple login page here

if __name__ == '__main__':
    app.run(debug=True)

