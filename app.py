from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import os

app = Flask(__name__)

try:
    model_path = os.getenv('MODEL_PATH', 'treatment_model.joblib')
    model = joblib.load(model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/doc')
def doc():
    return render_template('DocIndex.html')

@app.route('/patient')
def patient():
    return render_template('Patient.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        data = request.json
        features = pd.DataFrame([data['features']])
        prediction = model.predict(features)
        return jsonify({'prediction': prediction.tolist()})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/report', methods=['GET'])
def get_report():
    try:
        with open('report.txt', 'r') as f:
            report = f.read()
        return jsonify({'report': report})
    except FileNotFoundError:
        return jsonify({'error': 'Report file not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
