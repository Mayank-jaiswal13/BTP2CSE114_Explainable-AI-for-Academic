from pathlib import Path
import json
import math
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from functools import wraps
from datetime import datetime
import os

PROJECT_DIR = Path(__file__).resolve().parent
MODEL_PATH = PROJECT_DIR / "models" / "academic_risk_xgboost.json"

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

# Load the compact JSON model used for serverless inference
model = None
try:
    if MODEL_PATH.exists():
        model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    else:
        print(f"Model file not found at {MODEL_PATH}. Please run main.py first.")
except Exception as e:
    print(f"Error loading model: {e}")


def predict_risk_probability(features):
    """Return the positive-class probability from the exported XGBoost trees."""
    base_score = float(model["base_score"])
    margin = math.log(base_score / (1 - base_score))

    for tree in model["trees"]:
        node = tree
        while "leaf" not in node:
            value = features[node["split"]]
            branch_id = node["yes"] if value < float(node["split_condition"]) else node["no"]
            node = next(child for child in node["children"] if child["nodeid"] == branch_id)
        margin += float(node["leaf"])

    if margin >= 0:
        return 1 / (1 + math.exp(-margin))
    exp_margin = math.exp(margin)
    return exp_margin / (1 + exp_margin)

# Simple demo user database (replace with a database for production use)
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

        # Map the form fields to the feature names stored in the exported model.
        features = {
            'Age': float(data.get('age', 0)),
            'Gender': float(data.get('gender', 0)),
            'Ethnicity': float(data.get('ethnicity', 0)),
            'ParentalEducation': float(data.get('parental_education', 0)),
            'StudyTimeWeekly': float(data.get('study_time', 0)),
            'Absences': float(data.get('absences', 0)),
            'Tutoring': float(data.get('tutoring', 0)),
            'ParentalSupport': float(data.get('parental_support', 0)),
            'Extracurricular': float(data.get('extracurricular', 0)),
            'Sports': float(data.get('sports', 0)),
            'Music': float(data.get('music', 0)),
            'Volunteering': float(data.get('volunteering', 0))
        }

        risk_probability = predict_risk_probability(features)
        prediction = int(risk_probability >= 0.5)

        result = {
            'risk': 'At Risk' if prediction == 1 else 'Not At Risk',
            'risk_score': risk_probability * 100,
            'confidence': max(risk_probability, 1 - risk_probability) * 100,
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
    return jsonify(user_history[-10:])

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
