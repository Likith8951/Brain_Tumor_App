# 🧠 Brain Tumor Detection System

A comprehensive web application for brain tumor detection using AI/ML models with patient management and data storage capabilities.

## ✨ Features

### 🔐 Authentication System
- **Sign In/Sign Up**: Secure user authentication
- **Default Admin**: Email: `admin@123`, Password: `admin123`
- **Profile Management**: Create accounts with name, email, and password

### 👤 Patient Information Management
- **Comprehensive Patient Data**: Name, age, gender, date of birth
- **Medical Information**: Blood group, contact number
- **Vital Signs**: Heart rate and blood pressure monitoring
- **Data Validation**: Automatic age calculation and input validation

### 🧠 AI-Powered Tumor Detection
- **Hybrid Model**: Combines CNN (Deep Learning) + Random Forest
- **Multiple Algorithms**: CNN, SVM, Random Forest ensemble
- **Confidence Scoring**: Detailed confidence breakdown per model
- **Clinical Classification**: Benign/Malignant classification

### 🎯 Tumor Marking & Visualization
- **Automatic Tumor Marking**: Visual highlighting of detected tumor areas
- **Image Enhancement**: Improved image processing for better analysis
- **Before/After Comparison**: Original vs marked images
- **Confidence-based Marking**: Marking intensity based on detection confidence

### 📊 Data Management & Storage
- **SQLite Database**: Persistent data storage
- **Patient Records**: Complete patient history
- **Prediction History**: All analysis results stored
- **Tabular View**: Easy-to-read data table with search functionality
- **Export Ready**: Data structured for easy export/analysis

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
python run_app.py
```

Or directly:
```bash
python app.py
```

### Access the Application
- **URL**: http://localhost:5000
- **Default Login**: admin@123 / admin123

## 📋 Usage Workflow

1. **Login/Signup** → Access the system
2. **Patient Form** → Enter patient details and vital signs
3. **Image Upload** → Upload brain scan (MRI/CT)
4. **AI Analysis** → Get tumor detection results
5. **View Results** → See marked images and confidence scores
6. **Data Table** → Review all patient records and predictions

## 🏗️ System Architecture

### Database Schema
- **Users**: Authentication and profile management
- **Patients**: Patient demographic and medical data
- **Predictions**: AI analysis results and image paths

### AI Models
- **CNN Model**: Deep learning for image classification
- **Random Forest**: Traditional ML for feature-based analysis
- **Ensemble**: Weighted combination of multiple models

### Image Processing
- **Tumor Marking**: Computer vision-based tumor highlighting
- **Image Enhancement**: CLAHE and preprocessing
- **Multi-format Support**: JPEG, PNG, JPG support

## 📁 File Structure

```
├── app.py                 # Main Flask application
├── database.py           # Database operations
├── image_processing.py   # Image analysis and marking
├── model_utils.py        # AI model utilities
├── run_app.py           # Application launcher
├── requirements.txt     # Python dependencies
├── models/
│   ├── BrainTumor10epochs.h5  # CNN model
│   └── rf_model.joblib        # Random Forest model
├── templates/
│   ├── login.html           # Login page
│   ├── signup.html          # Registration page
│   ├── patient_form.html    # Patient data entry
│   ├── index.html           # Main analysis interface
│   └── data_table.html      # Data viewing interface
├── uploads/              # Uploaded images storage
└── data/                # Training dataset
```

## 🔧 Configuration

### Database
- **Type**: SQLite (brain_tumor_app.db)
- **Auto-initialization**: Creates tables on first run
- **Default Admin**: Automatically created

### Models
- **CNN**: Pre-trained brain tumor detection model
- **Random Forest**: Traditional ML model for comparison
- **Ensemble**: Configurable model weights (70% CNN + 30% RF)

### Security
- **Session Management**: Flask sessions for user state
- **Input Validation**: Form validation and sanitization
- **File Upload**: Secure file handling with type checking

## 📊 Data Features

### Patient Information Collected
- Personal: Name, age, gender, DOB, contact
- Medical: Blood group, heart rate, blood pressure
- Analysis: Tumor detection results, confidence scores
- Images: Original and marked scan images

### Data Export
- **Tabular Format**: Ready for CSV/Excel export
- **Search Functionality**: Filter by patient name
- **Historical Data**: Complete analysis history
- **Real-time Updates**: Auto-refresh capabilities

## 🎯 Tumor Detection Process

1. **Image Upload**: Patient scan uploaded
2. **Preprocessing**: Image enhancement and normalization
3. **AI Analysis**: Multiple models analyze the image
4. **Ensemble Prediction**: Weighted combination of results
5. **Tumor Marking**: Visual highlighting of detected areas
6. **Results Display**: Confidence scores and classification
7. **Data Storage**: Results saved to database

## 🔍 Model Performance

### CNN Model
- **Architecture**: Deep convolutional neural network
- **Training**: 10 epochs on brain tumor dataset
- **Output**: Tumor probability score

### Random Forest
- **Features**: Handcrafted image features
- **Trees**: Ensemble of decision trees
- **Output**: Classification probability

### Ensemble
- **Weighting**: 70% CNN + 30% Random Forest
- **Threshold**: 50% for tumor classification
- **Confidence**: Combined confidence scoring

## 🛡️ Security & Privacy

- **User Authentication**: Secure login system
- **Data Encryption**: Session-based security
- **File Validation**: Image type and size validation
- **Access Control**: User-specific data access

## 📱 User Interface

### Responsive Design
- **Mobile Friendly**: Works on all device sizes
- **Modern UI**: Clean, professional interface
- **Intuitive Navigation**: Easy-to-use workflow
- **Visual Feedback**: Progress indicators and status messages

### Accessibility
- **Form Validation**: Real-time input validation
- **Error Handling**: Clear error messages
- **Success Feedback**: Confirmation messages
- **Loading States**: Progress indicators

## 🔄 Future Enhancements

- **Multi-model Support**: Additional AI models
- **Advanced Marking**: More precise tumor localization
- **Report Generation**: PDF reports for patients
- **API Integration**: REST API for external systems
- **Advanced Analytics**: Statistical analysis dashboard

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Verify all required files are present
3. Ensure Python dependencies are installed
4. Check database permissions and file paths

## 📄 License

This is a prototype system for educational and research purposes. Not intended for clinical use without proper validation and regulatory approval.