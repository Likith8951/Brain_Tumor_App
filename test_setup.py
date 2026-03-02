#!/usr/bin/env python3
"""
Test script to verify the application setup
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("  ✅ Flask imported successfully")
    except ImportError:
        print("  ❌ Flask not found - run: pip install flask")
        return False
    
    try:
        import cv2
        print("  ✅ OpenCV imported successfully")
    except ImportError:
        print("  ❌ OpenCV not found - run: pip install opencv-python")
        return False
    
    try:
        import sqlite3
        print("  ✅ SQLite3 available")
    except ImportError:
        print("  ❌ SQLite3 not available")
        return False
    
    try:
        from database import init_database
        print("  ✅ Database module imported")
    except ImportError as e:
        print(f"  ❌ Database module error: {e}")
        return False
    
    try:
        from image_processing import mark_tumor_in_image
        print("  ✅ Image processing module imported")
    except ImportError as e:
        print(f"  ❌ Image processing module error: {e}")
        return False
    
    return True

def test_database():
    """Test database initialization"""
    print("\n💾 Testing database...")
    
    try:
        from database import init_database, get_user
        
        # Initialize database
        init_database()
        print("  ✅ Database initialized successfully")
        
        # Test admin user
        admin = get_user('admin@123', 'admin123')
        if admin:
            print("  ✅ Default admin user found")
        else:
            print("  ❌ Default admin user not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Database error: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        'app.py',
        'database.py',
        'image_processing.py',
        'templates/login.html',
        'templates/signup.html',
        'templates/patient_form.html',
        'templates/index.html',
        'templates/data_table.html'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n❌ {len(missing_files)} files missing!")
        return False
    else:
        print(f"\n✅ All {len(required_files)} required files found!")
        return True

def test_directories():
    """Test if required directories exist"""
    print("\n📂 Testing directories...")
    
    required_dirs = ['uploads', 'templates', 'models']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name) and os.path.isdir(dir_name):
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ - MISSING")
            # Create missing directories
            os.makedirs(dir_name, exist_ok=True)
            print(f"  ✅ Created {dir_name}/")
    
    return True

def main():
    """Run all tests"""
    print("🧠 Brain Tumor Detection - Setup Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Directories", test_directories),
        ("Python Imports", test_imports),
        ("Database", test_database),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} test PASSED")
            else:
                print(f"❌ {test_name} test FAILED")
        except Exception as e:
            print(f"❌ {test_name} test ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Application is ready to run.")
        print("🚀 Run: python app.py")
        print("🌐 Access: http://localhost:5000")
        print("🔑 Login: admin@123 / admin123")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)