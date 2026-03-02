import sqlite3
import os
from datetime import datetime

DATABASE_PATH = 'brain_tumor_app.db'

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Patient data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            date_of_birth DATE NOT NULL,
            blood_group TEXT NOT NULL,
            contact_number TEXT NOT NULL,
            heart_rate INTEGER NOT NULL,
            blood_pressure TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Predictions table to store results
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            diagnosis TEXT NOT NULL,
            confidence_overall REAL NOT NULL,
            confidence_cnn REAL NOT NULL,
            confidence_rf REAL NOT NULL,
            confidence_svm REAL NOT NULL,
            confidence_ensemble REAL NOT NULL,
            clinical_classification TEXT,
            tumor_marked_image TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')
    
    # Insert default admin user
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password, name) 
        VALUES (?, ?, ?)
    ''', ('admin@123', 'admin123', 'Administrator'))
    
    conn.commit()
    conn.close()

def get_user(email, password):
    """Authenticate user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user

def create_user(email, password, name):
    """Create new user"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, password, name) VALUES (?, ?, ?)', 
                      (email, password, name))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def create_patient(name, age, gender, dob, blood_group, contact, heart_rate, blood_pressure):
    """Create new patient record"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (name, age, gender, date_of_birth, blood_group, 
                            contact_number, heart_rate, blood_pressure)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, gender, dob, blood_group, contact, heart_rate, blood_pressure))
    conn.commit()
    patient_id = cursor.lastrowid
    conn.close()
    return patient_id

def save_prediction(patient_id, image_path, diagnosis, confidence_overall, 
                   confidence_cnn, confidence_rf, confidence_svm, confidence_ensemble,
                   clinical_classification, tumor_marked_image=None):
    """Save prediction results"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (patient_id, image_path, diagnosis, confidence_overall,
                               confidence_cnn, confidence_rf, confidence_svm, confidence_ensemble,
                               clinical_classification, tumor_marked_image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (patient_id, image_path, diagnosis, confidence_overall, confidence_cnn, 
          confidence_rf, confidence_svm, confidence_ensemble, clinical_classification, tumor_marked_image))
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    return prediction_id

def get_all_predictions():
    """Get all predictions with patient data"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, pt.name, pt.age, pt.gender, pt.blood_group, pt.contact_number,
               p.diagnosis, p.confidence_overall, p.clinical_classification, p.created_at
        FROM predictions p
        JOIN patients pt ON p.patient_id = pt.id
        ORDER BY p.created_at DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return results

def get_patient_by_id(patient_id):
    """Get patient details by ID"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    return patient