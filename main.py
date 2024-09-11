from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/hospital_management"
mongo = PyMongo(app)

# Hardcoded credentials (unchanged)
HARDCODED_EMAIL = "deepesh55@gmail.com"
HARDCODED_PASSWORD_HASH = generate_password_hash("deep55")

@app.route('/')
def index():
    return redirect(url_for('login'))

# Login route (unchanged)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == HARDCODED_EMAIL and check_password_hash(HARDCODED_PASSWORD_HASH, password):
            session['user_id'] = 'hardcoded_user_id'
            session['email'] = HARDCODED_EMAIL
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Logout route (unchanged)
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

# Home/Dashboard route (unchanged)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))
    
    return render_template('home.html')

# Patients page (unchanged)
@app.route('/patients')
def patients():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    # Fetch all patients from the database
    patients = mongo.db.patients.find()
    return render_template('patients.html', patients=patients)

# Updated add_patient route
@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        patient = {
            'name': request.form.get('name'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'contact': request.form.get('contact'),
            'address': request.form.get('address'),
            'emergency_contact': request.form.get('emergency_contact'),
            'medical_history': request.form.get('medical_history'),
            'allergies': request.form.get('allergies'),
            'current_medications': request.form.get('current_medications'),
            'insurance_details': request.form.get('insurance_details'),
            'admission_date': request.form.get('admission_date'),
            'discharge_date': request.form.get('discharge_date'),
            'admission_status': request.form.get('admission_status'),
            'ward_room': request.form.get('ward_room'),
            'diagnosis': request.form.get('diagnosis'),
            'treatment_plan': request.form.get('treatment_plan'),
            'lab_results': request.form.get('lab_results'),
            'doctor_alloted': request.form.get('doctor_alloted'),
            'nursing_notes': request.form.get('nursing_notes'),
            'physician_notes': request.form.get('physician_notes'),
            'follow_up_appointments': request.form.get('follow_up_appointments'),
            'discharge_summary': request.form.get('discharge_summary'),
            'status': request.form.get('status'),
            'last_update': request.form.get('last_update'),
            'treatment_outcomes': request.form.get('treatment_outcomes'),
            'patient_consent': request.form.get('patient_consent'),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        mongo.db.patients.insert_one(patient)
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients'))

    return render_template('add_patient.html')

# Updated edit_patient route
@app.route('/edit_patient/<id>', methods=['GET', 'POST'])
def edit_patient(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    patient = mongo.db.patients.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        updated_patient = {
            'name': request.form.get('name'),
            'dob': request.form.get('dob'),
            'gender': request.form.get('gender'),
            'contact': request.form.get('contact'),
            'address': request.form.get('address'),
            'emergency_contact': request.form.get('emergency_contact'),
            'medical_history': request.form.get('medical_history'),
            'allergies': request.form.get('allergies'),
            'current_medications': request.form.get('current_medications'),
            'insurance_details': request.form.get('insurance_details'),
            'admission_date': request.form.get('admission_date'),
            'discharge_date': request.form.get('discharge_date'),
            'admission_status': request.form.get('admission_status'),
            'ward_room': request.form.get('ward_room'),
            'diagnosis': request.form.get('diagnosis'),
            'treatment_plan': request.form.get('treatment_plan'),
            'lab_results': request.form.get('lab_results'),
            'doctor_alloted': request.form.get('doctor_alloted'),
            'nursing_notes': request.form.get('nursing_notes'),
            'physician_notes': request.form.get('physician_notes'),
            'follow_up_appointments': request.form.get('follow_up_appointments'),
            'discharge_summary': request.form.get('discharge_summary'),
            'status': request.form.get('status'),
            'last_update': request.form.get('last_update'),
            'treatment_outcomes': request.form.get('treatment_outcomes'),
            'patient_consent': request.form.get('patient_consent'),
            'updated_at': datetime.now()
        }
        mongo.db.patients.update_one({'_id': ObjectId(id)}, {'$set': updated_patient})
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients'))

    return render_template('edit_patient.html', patient=patient)

# Delete patient route (unchanged)
@app.route('/delete_patient/<id>')
def delete_patient(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    mongo.db.patients.delete_one({'_id': ObjectId(id)})
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('patients'))

if __name__ == '__main__':
    app.run(debug=True)
