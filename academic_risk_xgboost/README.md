# 🎓 Academic Risk Prediction System - Professional Web Interface

A sophisticated machine learning application that predicts student academic risk using XGBoost. Features a modern, professional web interface designed for educators, counselors, and administrators.

## ✨ Features

### 🎯 Core Functionality
- **Advanced Predictions**: Uses trained XGBoost model to predict academic risk
- **12-Factor Analysis**: Analyzes multiple student attributes including:
  - Personal information (age, gender, ethnicity)
  - Family background (parental education, support)
  - Academic metrics (study time, absences, tutoring)
  - Extracurricular activities (sports, music, volunteering)

### 🎨 User Interface Highlights
- **Modern Gradient Design**: Professional purple-to-blue gradient theme
- **Responsive Layout**: Fully responsive design works on desktop, tablet, and mobile
- **Interactive Forms**: Intuitive form with organized sections and validation
- **Real-time Results**: Instant predictions with visual risk indicators
- **Performance Metrics**: Display of model accuracy, precision, recall, and F1-score
- **Smooth Animations**: Professional transitions and visual feedback

### 🔒 Security
- **Multi-user Support**: Role-based access (admin, educator, counselor)
- **Session Management**: Secure login and logout
- **Prediction History**: Tracks user prediction history

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip package manager

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Train the Model
First, ensure you have trained the XGBoost model:
```bash
python main.py
```

This will create `academic_risk_xgboost.pkl` required by the web app.

### 4. Run the Web Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### 5. Login with Demo Credentials
- **Admin**: admin / admin123
- **Educator**: educator / educator@123
- **Counselor**: counselor / counselor@123

## 📁 Project Structure
```
academic_risk_xgboost/
├── app.py                          # Flask web application
├── main.py                         # Model training script
├── requirements.txt                # Python dependencies
├── academic_risk_xgboost.pkl       # Trained model (generated)
├── Student_performance_data_.csv   # Training data
├── templates/
│   ├── base.html                   # Base template with navbar
│   ├── login.html                  # Professional login page
│   └── dashboard.html              # Main prediction dashboard
└── static/
    ├── css/
    │   └── style.css               # Professional styling
    └── js/
        └── main.js                 # Interactive functionality
```

## 🎮 How to Use

### Making Predictions
1. **Log in** with your credentials
2. **Fill in student information** across organized sections:
   - Personal Information
   - Academic Information
   - Extracurricular Activities
3. **Click "Predict Risk"** button
4. **View results** with:
   - Risk status (At Risk / Safe)
   - Risk score percentage
   - Confidence level
   - Personalized recommendations

### Understanding Results

**Risk Indicator States:**
- 🟢 **SAFE**: Student is performing well (risk score < 50%)
- 🔴 **AT RISK**: Student shows academic risk indicators (risk score ≥ 50%)

**Risk Meter**: Visual representation of risk probability (0-100%)

**Recommendations**: Automatically generated guidance based on prediction

## 📊 Model Performance

The XGBoost model achieves excellent results:
- **Accuracy**: 92.69%
- **Precision**: 0.92
- **Recall**: 0.93
- **F1-Score**: 0.93

Validated on 479 test samples with comprehensive evaluation metrics.

## 🛠️ Customization

### Adding New Users
Edit the `USERS` dictionary in `app.py`:
```python
USERS = {
    'admin': 'admin123',
    'educator': 'educator@123',
    'counselor': 'counselor@123',
    'your_user': 'your_password'  # Add here
}
```

### Changing Colors/Theme
Modify the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;      /* Main purple */
    --secondary-color: #764ba2;    /* Darker purple */
    --success-color: #27ae60;      /* Green for safe */
    --danger-color: #e74c3c;       /* Red for risk */
}
```

### Modifying Features
Update the feature list in both:
- `templates/dashboard.html` (form fields)
- `app.py` (prediction function)

## 📈 System Requirements

**Minimum:**
- 2GB RAM
- 500MB disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)

**Recommended:**
- 4GB+ RAM
- 1GB disk space
- Latest browser versions

## 🌐 Accessing from Other Devices

To access from another machine on your network:

1. Run the app with:
   ```bash
   python app.py
   ```

2. Access from other device:
   ```
   http://<your_machine_ip>:5000
   ```

## 🐛 Troubleshooting

### Model Not Loading
- Ensure `academic_risk_xgboost.pkl` exists
- Run `python main.py` to train the model
- Check file permissions

### Port Already in Use
```bash
# Use a different port
python -c "from app import app; app.run(port=5001)"
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## 📝 Data Requirements

The prediction form requires 12 student attributes:
1. **Age**: 15-30 years
2. **Gender**: Male, Female, Other
3. **Ethnicity**: 5 categories
4. **Parental Education**: High School to PhD
5. **Study Time**: Hours per week
6. **Absences**: Days per year
7. **Tutoring**: Yes/No
8. **Parental Support**: Low, Medium, High
9. **Extracurricular**: Yes/No
10. **Sports**: Yes/No
11. **Music**: Yes/No
12. **Volunteering**: Yes/No

## 🔐 Security Notes

⚠️ **Important for Production:**
- Change the `app.secret_key` in `app.py`
- Use a proper database instead of in-memory storage
- Implement proper password hashing (use werkzeug.security)
- Enable HTTPS in production
- Set `debug=False` before deployment

## 📚 Technical Stack

- **Backend**: Flask (Python web framework)
- **ML Model**: XGBoost classifier
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: In-memory (demo) - Use PostgreSQL/MongoDB for production
- **Authentication**: Session-based

## 🎓 Educational Use

Perfect for:
- 📊 Student success initiatives
- 🏫 Academic advising
- 📋 Early warning systems
- 👨‍🎓 Student retention programs
- 🔬 Machine learning demonstrations

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask documentation
3. Verify model file exists
4. Check browser console for JavaScript errors

## 📄 License

This project is provided as-is for educational and research purposes.

---

**Built with ❤️ for Academic Success**

*Last Updated: May 2024*
