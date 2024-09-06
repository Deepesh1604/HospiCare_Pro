from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/hospital_management"
app.secret_key = "your_secret_key"  # Change this to a secure random key in production

mongo = PyMongo(app)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = mongo.db.users.find_one({"email": email})
        
        if user and check_password_hash(user['password'], password):
            # Login successful
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Create a dashboard route
        else:
            # Login failed
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)