from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  

# Hardcoded credentials
HARDCODED_EMAIL = "deepesh55@gmail.com"
HARDCODED_PASSWORD_HASH = generate_password_hash("deep55")  # Hash of the hardcoded password

@app.route('/')
def index():
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the entered email and password match the hardcoded credentials
        if email == HARDCODED_EMAIL and check_password_hash(HARDCODED_PASSWORD_HASH, password):
            # Set session and log the user in
            session['user_id'] = 'hardcoded_user_id'
            session['email'] = HARDCODED_EMAIL
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # If login fails
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    # Clear session
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Home/Dashboard route
@app.route('/dashboard')
def dashboard():
    # If user not logged in, redirect to login
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('home.html')

# Patient route
@app.route('/patient')
def patient():
    # Only accessible if logged in
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    return render_template('patient.html')

# Doctor route
@app.route('/doctor')
def doctor():
    # Only accessible if logged in
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    return render_template('doctor.html')

# Billing route
@app.route('/billing')
def billing():
    # Only accessible if logged in
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    return render_template('billing.html')

# Appointment route
@app.route('/appointment')
def appointment():
    # Only accessible if logged in
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    return render_template('appointment.html')

if __name__ == '__main__':
    app.run(debug=True)
