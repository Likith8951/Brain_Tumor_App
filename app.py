import os
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory
import cv2
import joblib
from datetime import datetime

from model_utils import load_deep_model, preprocess_for_deep, extract_handcrafted_features
from database import (
    init_database, get_user, create_user, create_patient,
    save_prediction, get_all_predictions
)
from image_processing import mark_tumor_in_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'change-this-secret-key'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize DB
init_database()

# Load models
deep_model, model_input_shape = load_deep_model('models/BrainTumor10epochs.h5') 

rf_model = None
if os.path.exists('models/rf_model.joblib'):
    rf_model = joblib.load('models/rf_model.joblib')

# ---------------- UTILITY ROUTES ---------------- #

# Route to serve uploaded files from the 'uploads' folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Route to reset current patient data and start a new form
@app.route('/reset-patient')
def reset_patient():
    if 'patient_data' in session:
        session.pop('patient_data')
    if 'patient_db_id' in session:
        session.pop('patient_db_id')
    return redirect(url_for('patient_form'))

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('patient_form'))

# ---------------- LOGIN, SIGNUP, LOGOUT routes (omitted for brevity) ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return render_template('login.html', error="All fields are required")

        user = get_user(email, password)
        if user:
            session['user_id'] = user[0]
            session['user_name'] = user[3]
            return redirect(url_for('patient_form'))

        return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return render_template('signup.html', error="All fields are required")

        user_id = create_user(email, password, name)
        if user_id:
            return render_template(
                'login.html',
                success="Account created successfully! Please login."
            )

        return render_template('signup.html', error="Email already exists")

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- PATIENT FORM ---------------- #

@app.route('/patient-form', methods=['GET', 'POST'])
def patient_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            age = int(request.form.get('age'))
            heart_rate = int(request.form.get('heart_rate'))
        except ValueError:
            return render_template('patient_form.html', error="Age and Heart Rate must be valid numbers")

        # Store patient data in session (transient)
        session['patient_data'] = {
            'name': request.form.get('name'),
            'age': age,
            'gender': request.form.get('gender'),
            'dob': request.form.get('dob'),
            'blood_group': request.form.get('blood_group'),
            'contact': request.form.get('contact'),
            'heart_rate': heart_rate,
            'blood_pressure': request.form.get('blood_pressure')
        }
        
        # Ensure any old patient ID is cleared when submitting a *new* form
        if 'patient_db_id' in session:
             session.pop('patient_db_id') 

        return redirect(url_for('analysis'))

    return render_template('patient_form.html')

# ---------------- ANALYSIS ---------------- #

@app.route('/analysis')
def analysis():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Allow access if we have either patient info (before first submission) 
    # OR patient ID (after first submission)
    if 'patient_data' not in session and 'patient_db_id' not in session:
        return redirect(url_for('patient_form'))

    # Pass patient data for the banner display
    patient_data_for_display = session.get('patient_data', {})
    
    return render_template('index.html', patient_data=patient_data_for_display)

# ---------------- DATA TABLE ---------------- #

@app.route('/data-table')
def data_table():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    predictions = get_all_predictions()
    return render_template('data_table.html', predictions=predictions)

# ---------------- PREDICT ---------------- #

@app.route('/predict', methods=['POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    # Patient Data Persistence Logic (Fix for "take patient data only once")
    if 'patient_data' not in session and 'patient_db_id' not in session:
        return redirect(url_for('patient_form'))

    # Get data structure for display/initial DB creation
    patient = session.get('patient_data')

    if 'patient_db_id' not in session:
        # FIRST submission: Create the patient record and store the ID.
        patient_id = create_patient(
            patient['name'], patient['age'], patient['gender'],
            patient['dob'], patient['blood_group'], patient['contact'],
            patient['heart_rate'], patient['blood_pressure']
        )
        session['patient_db_id'] = patient_id # Store the new ID for subsequent predictions!
    else:
        # Subsequent submission: Use the stored ID.
        patient_id = session['patient_db_id']
        
    
    file = request.files.get('image')
    if not file:
        return render_template(
            'index.html',
            patient_data=patient,
            error_message="No image file selected for analysis."
        )

    # 1. Save original file and read it
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    img = cv2.imread(filepath)
    if img is None:
        return "Invalid image", 400

    # 2. Get predictions
    x = preprocess_for_deep(img, model_input_shape)
    p_deep = float(deep_model.predict(x)[0][-1])

    if rf_model:
        feat = extract_handcrafted_features(img)
        p_rf = float(rf_model.predict_proba([feat])[0][1])
    else:
        p_rf = 0.5

    p_final = 0.7 * p_deep + 0.3 * p_rf
    label = "Tumor" if p_final >= 0.5 else "No Tumor"

    # Final overall confidence for display
    confidence = round(p_final * 100, 1)

    # 3. Mark tumor if applicable
    marked_img_path = None
    if label == "Tumor":
        marked_img_path = mark_tumor_in_image(filepath, confidence)

    # 4. Save prediction data (using the determined patient_id)
    p_deep_perc = p_deep * 100
    p_rf_perc = p_rf * 100
    p_combined_perc = (p_deep + p_rf) * 50
    clinical_classification = "Benign" if p_final < 0.75 else "Malignant"
    diagnosis = label

    save_prediction(
        patient_id, filepath, label, confidence,
        p_deep_perc, p_rf_perc,
        p_combined_perc, confidence,
        clinical_classification,
        marked_img_path
    )

    # DO NOT POP 'patient_data' or 'patient_db_id'. Keep them for subsequent uploads.
    
    # 5. Prepare URLs and final template variables
    original_img_url = url_for('uploaded_file', filename=os.path.basename(filepath))
    marked_img_url = url_for('uploaded_file', filename=os.path.basename(marked_img_path)) if marked_img_path else None
    
    # Pass data to match index.html variable names
    return render_template(
        'index.html',
        # Image URLs
        img_url=original_img_url,
        marked_img_url=marked_img_url,
        
        # Prediction Data
        label=label,
        diagnosis=diagnosis,
        clinical_classification=clinical_classification,
        
        confidence_overall=confidence,
        confidence_cnn=round(p_deep_perc, 1),
        confidence_rf=round(p_rf_perc, 1),
        confidence_ensemble=confidence,
        
        # Patient Data (still in session)
        patient_data=patient,
        patient_name=patient['name'] if patient else 'Unknown Patient',
        show_success=True
    )

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)