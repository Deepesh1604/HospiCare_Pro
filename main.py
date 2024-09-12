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

    patients = mongo.db.patients.find()
    return render_template('patients.html', patients=patients)

# Updated add_patient route (unchanged)
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

# Updated edit_patient route (unchanged)
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

# New routes for doctor management

@app.route('/doctor')
def doctor():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    doctor = mongo.db.doctor.find()
    return render_template('doctor.html', doctor=doctor)

@app.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        doctor = {
            'name': request.form.get('name'),
            'specialization': request.form.get('specialization'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'license_number': request.form.get('license_number'),
            'joining_date': request.form.get('joining_date'),
            'qualifications': request.form.get('qualifications'),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        mongo.db.doctor.insert_one(doctor)
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctor'))

    return render_template('add_doctor.html')

@app.route('/edit_doctor/<id>', methods=['GET', 'POST'])
def edit_doctor(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    doctor = mongo.db.doctor.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        updated_doctor = {
            'name': request.form.get('name'),
            'specialization': request.form.get('specialization'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'address': request.form.get('address'),
            'license_number': request.form.get('license_number'),
            'joining_date': request.form.get('joining_date'),
            'qualifications': request.form.get('qualifications'),
            'updated_at': datetime.now()
        }
        mongo.db.doctor.update_one({'_id': ObjectId(id)}, {'$set': updated_doctor})
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('doctor'))

    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/delete_doctor/<id>')
def delete_doctor(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    mongo.db.doctor.delete_one({'_id': ObjectId(id)})
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('doctor'))
@app.route('/billing')
def billing():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    bills = mongo.db.billing.find()
    return render_template('billing.html', bills=bills)

@app.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        bill = {
            'patient_id': request.form.get('patient_id'),
            'patient_name': request.form.get('patient_name'),
            'doctor_name': request.form.get('doctor_name'),
            'service_date': request.form.get('service_date'),
            'description': request.form.get('description'),
            'amount': float(request.form.get('amount')),
            'payment_status': request.form.get('payment_status'),
            'payment_method': request.form.get('payment_method'),
            'insurance_claim': request.form.get('insurance_claim'),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        mongo.db.billing.insert_one(bill)
        flash('Bill added successfully!', 'success')
        return redirect(url_for('billing'))

    patients = mongo.db.patients.find({}, {'_id': 1, 'name': 1})
    doctors = mongo.db.doctors.find({}, {'_id': 1, 'name': 1})
    return render_template('add_bill.html', patients=patients, doctors=doctors)

@app.route('/edit_bill/<id>', methods=['GET', 'POST'])
def edit_bill(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    bill = mongo.db.billing.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        updated_bill = {
            'patient_id': request.form.get('patient_id'),
            'patient_name': request.form.get('patient_name'),
            'doctor_name': request.form.get('doctor_name'),
            'service_date': request.form.get('service_date'),
            'description': request.form.get('description'),
            'amount': float(request.form.get('amount')),
            'payment_status': request.form.get('payment_status'),
            'payment_method': request.form.get('payment_method'),
            'insurance_claim': request.form.get('insurance_claim'),
            'updated_at': datetime.now()
        }
        mongo.db.billing.update_one({'_id': ObjectId(id)}, {'$set': updated_bill})
        flash('Bill updated successfully!', 'success')
        return redirect(url_for('billing'))

    patients = mongo.db.patients.find({}, {'_id': 1, 'name': 1})
    doctors = mongo.db.doctors.find({}, {'_id': 1, 'name': 1})
    return render_template('edit_bill.html', bill=bill, patients=patients, doctors=doctors)

@app.route('/delete_bill/<id>')
def delete_bill(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    mongo.db.billing.delete_one({'_id': ObjectId(id)})
    flash('Bill deleted successfully!', 'success')
    return redirect(url_for('billing'))

if __name__ == '__main__':
    app.run(debug=True)