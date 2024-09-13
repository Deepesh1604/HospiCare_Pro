from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/hospital_management"
app.config["MONGO_CONNECT_TIMEOUT_MS"] = 30000  # 30 seconds
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
            'follow_up_appointment': request.form.get('follow_up_appointment'),
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
            'follow_up_appointment': request.form.get('follow_up_appointment'),
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

    bills = mongo.db.bills.find()
    paid_count = mongo.db.bills.count_documents({"status": "Paid"})
    pending_count = mongo.db.bills.count_documents({"status": "Pending"})
    total_count = mongo.db.bills.count_documents({})

    return render_template('billing.html', bills=bills, paid_count=paid_count, pending_count=pending_count, total_count=total_count)

@app.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        bill = {
            'bill_number': request.form.get('bill_number'),
            'patient_name': request.form.get('patient_name'),
            'date': request.form.get('date'),
            'amount': float(request.form.get('amount')),
            'status': request.form.get('status'),
            'description': request.form.get('description'),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        mongo.db.bills.insert_one(bill)
        flash('Bill added successfully!', 'success')
        return redirect(url_for('billing'))

    return render_template('add_bill.html')

@app.route('/edit_bill/<id>', methods=['GET', 'POST'])
def edit_bill(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    bill = mongo.db.bills.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        updated_bill = {
            'bill_number': request.form.get('bill_number'),
            'patient_name': request.form.get('patient_name'),
            'date': request.form.get('date'),
            'amount': float(request.form.get('amount')),
            'status': request.form.get('status'),
            'description': request.form.get('description'),
            'updated_at': datetime.now()
        }
        mongo.db.bills.update_one({'_id': ObjectId(id)}, {'$set': updated_bill})
        flash('Bill updated successfully!', 'success')
        return redirect(url_for('billing'))

    return render_template('edit_bill.html', bill=bill)

@app.route('/delete_bill/<id>')
def delete_bill(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    mongo.db.bills.delete_one({'_id': ObjectId(id)})
    flash('Bill deleted successfully!', 'success')
    return redirect(url_for('billing'))

@app.route('/search_bill', methods=['POST'])
def search_bill():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    bill_number = request.form.get('bill_number')
    bill = mongo.db.bills.find_one({'bill_number': bill_number})

    if bill:
        return render_template('billing.html', bills=[bill], show_all_link=True)
    else:
        flash('Bill not found', 'error')
        return redirect(url_for('billing'))

@app.route('/appointment')
def appointment():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    appointment = mongo.db.appointment.find()
    scheduled_count = mongo.db.appointment.count_documents({"status": "Scheduled"})
    completed_count = mongo.db.appointment.count_documents({"status": "Completed"})
    total_count = mongo.db.appointment.count_documents({})

    return render_template('appointment.html', appointment=appointment, scheduled_count=scheduled_count, completed_count=completed_count, total_count=total_count)

@app.route('/add_appointment', methods=['GET', 'POST'])
def add_appointment():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        appointment = {
            'appointment_id': request.form.get('appointment_id'),
            'patient_name': request.form.get('patient_name'),
            'doctor_name': request.form.get('doctor_name'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'status': request.form.get('status'),
            'notes': request.form.get('notes'),
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        mongo.db.appointment.insert_one(appointment)
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('appointment'))

    return render_template('add_appointment.html')

@app.route('/edit_appointment/<id>', methods=['GET', 'POST'])
def edit_appointment(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    appointment = mongo.db.appointment.find_one({'_id': ObjectId(id)})

    if request.method == 'POST':
        updated_appointment = {
            'appointment_id': request.form.get('appointment_id'),
            'patient_name': request.form.get('patient_name'),
            'doctor_name': request.form.get('doctor_name'),
            'date': request.form.get('date'),
            'time': request.form.get('time'),
            'status': request.form.get('status'),
            'notes': request.form.get('notes'),
            'updated_at': datetime.now()
        }
        mongo.db.appointment.update_one({'_id': ObjectId(id)}, {'$set': updated_appointment})
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointment'))

    return render_template('edit_appointment.html', appointment=appointment)

@app.route('/delete_appointment/<id>')
def delete_appointment(id):
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    mongo.db.appointment.delete_one({'_id': ObjectId(id)})
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('appointment'))

@app.route('/search_appointment', methods=['POST'])
def search_appointment():
    if 'user_id' not in session:
        flash('Please log in to access this page', 'error')
        return redirect(url_for('login'))

    appointment_id = request.form.get('appointment_id')
    appointment = mongo.db.appointment.find_one({'appointment_id': appointment_id})

    if appointment:
        return render_template('appointment.html', appointment=[appointment], show_all_link=True)
    else:
        flash('Appointment not found', 'error')
        return redirect(url_for('appointments'))
if __name__ == '__main__':
    app.run(debug=True)