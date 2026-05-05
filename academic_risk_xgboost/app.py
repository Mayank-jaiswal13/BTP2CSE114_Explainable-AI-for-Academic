from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'academic_risk_secret_key_2024'

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
    volunteering = st.selectbox("Volunteering", [0, 1],
                                format_func=lambda x: "No" if x == 0 else "Yes")

st.markdown("---")

# ── PREDICT ───────────────────────────────────────────────
if st.button("🔍 Predict Academic Risk", use_container_width=True):

    input_data = np.array([[age, gender, ethnicity, parental_education,
                            study_time, absences, tutoring, parental_support,
                            extracurricular, sports, music, volunteering]])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]

    st.markdown("---")
    st.subheader("📊 Prediction Result")

    col_a, col_b = st.columns(2)

    with col_a:
        if prediction == 1:
            st.error("⚠️ This student is AT RISK academically")
            st.metric("Risk Probability", f"{probability[1]:.1%}")
        else:
            st.success("✅ This student is NOT at risk academically")
            st.metric("Safe Probability", f"{probability[0]:.1%}")

    with col_b:
        st.metric("At Risk Probability", f"{probability[1]:.1%}")
        st.metric("Not At Risk Probability", f"{probability[0]:.1%}")

    # ── SHAP EXPLANATION ──────────────────────────────────
    st.markdown("---")
    st.subheader("🔎 Why this prediction? (SHAP Explanation)")
    st.markdown("*Red bars push toward At Risk. Blue bars push toward Not At Risk.*")

    shap_values = explainer(input_data)  # Returns Explanation object directly

    fig, ax = plt.subplots(figsize=(10, 5))
    shap.waterfall_plot(shap_values[0], show=False)  # Use first sample
    st.pyplot(fig)
    plt.close()

    st.markdown("---")
    st.caption("Model: XGBoost (Tuned) | Accuracy: 93.32% | At-Risk Recall: 0.94 | Indian Grading: GPA < 2.0")
