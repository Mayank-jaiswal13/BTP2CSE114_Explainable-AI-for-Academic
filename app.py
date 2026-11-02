from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(32)

# Load the trained model
model = None
try:
    if os.path.exists('academic_risk_xgboost.pkl'):
        model = joblib.load('academic_risk_xgboost.pkl')
    else:
        print("⚠️ Model file not found. Please run main.py first to train the model.")
except Exception as e:
    print(f"❌ Error loading model: {e}")

# Simple user database (for scalability, use real database)
USERS = {
    'admin': 'admin123',
    'educator': 'educator@123',
    'counselor': 'counselor@123'
}

# Prediction history
prediction_history = []

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle logout parameter
    logout_param = request.args.get('logout')
    if logout_param:
        session.pop('user', None)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=session['user'])

@app.route('/predict', methods=['POST'])
@login_required
def predict():
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded. Please train the model first.'}), 400
        
        data = request.json
        
        # Extract features in the correct order
        features = [
            float(data.get('age', 0)),
            float(data.get('gender', 0)),
            float(data.get('ethnicity', 0)),
            float(data.get('parental_education', 0)),
            float(data.get('study_time', 0)),
            float(data.get('absences', 0)),
            float(data.get('tutoring', 0)),
            float(data.get('parental_support', 0)),
            float(data.get('extracurricular', 0)),
            float(data.get('sports', 0)),
            float(data.get('music', 0)),
            float(data.get('volunteering', 0))
        ]
        
        # Make prediction
        features_array = np.array([features])
        prediction = model.predict(features_array)[0]
        probability = model.predict_proba(features_array)[0]
        
        result = {
            'risk': 'At Risk' if prediction == 1 else 'Not At Risk',
            'risk_score': float(probability[1]) * 100,
            'confidence': max(float(probability[0]), float(probability[1])) * 100,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Store in history
        prediction_history.append({
            'user': session['user'],
            'data': data,
            'result': result
        })
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/history')
@login_required
def get_history():
    user_history = [h for h in prediction_history if h['user'] == session['user']]
    return jsonify(user_history[-10:])  # Return last 10 predictions

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
