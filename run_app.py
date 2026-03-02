#!/usr/bin/env python3
"""
Simple script to run the Brain Tumor Detection application
"""

import os
import sys

def main():
    print("🧠 Starting Brain Tumor Detection Application...")
    print("=" * 50)
    
    # Check if required files exist
    required_files = [
        'app.py',
        'database.py', 
        'image_processing.py',
        'model_utils.py',
        'models/BrainTumor10epochs.h5',
        'templates/login.html',
        'templates/signup.html',
        'templates/patient_form.html',
        'templates/index.html',
        'templates/data_table.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all files are present before running.")
        return
    
    print("✅ All required files found!")
    print("\n📋 Application Features:")
    print("   1. 🔐 User Authentication (admin@123 / admin123)")
    print("   2. 👤 Patient Information Form")
    print("   3. 🧠 Brain Tumor Detection with AI")
    print("   4. 🎯 Tumor Marking in Images")
    print("   5. 📊 Data Storage & Retrieval")
    print("   6. 📈 Tabular Data View")
    
    print("\n🚀 Starting Flask application...")
    print("📱 Access the app at: http://localhost:5000")
    print("🔑 Default login: admin@123 / admin123")
    print("\n" + "=" * 50)
    
    # Import and run the Flask app
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        print("Please check that all dependencies are installed.")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()