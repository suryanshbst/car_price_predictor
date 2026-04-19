from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# 1. PATH MANAGEMENT
# This tells Python to always look in the current folder, regardless of where the app is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(BASE_DIR, 'Cleaned_Car_data.csv')
model_path = os.path.join(BASE_DIR, 'LinearRegressionModel.pkl')

# 2. SAFETY CHECKS (Defensive Programming)
if not os.path.exists(data_path):
    print(f"CRITICAL ERROR: Data file not found at {data_path}")
    car_data = None
else:
    car_data = pd.read_csv(data_path)
    print("✅ Data loaded successfully.")

if not os.path.exists(model_path):
    print(f"WARNING: Model file not found at {model_path}. Train the model first!")
    model = None
else:
    model = pickle.load(open(model_path, 'rb'))
    print("✅ Model loaded successfully.")

# 3. API ENDPOINTS
@app.route('/api/options', methods=['GET'])
def get_options():
    if car_data is None:
        return jsonify({"error": "Data file not loaded"}), 500
        
    try:
        # Build the company-to-model map for the cascading dropdowns
        company_model_map = car_data.groupby('company')['name'].unique().apply(list).to_dict()
        
        return jsonify({
            "companies": sorted(car_data['company'].unique().tolist()),
            "company_model_map": company_model_map,
            "years": sorted(car_data['year'].unique().tolist(), reverse=True),
            "fuel_types": car_data['fuel_type'].dropna().unique().tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500
        
    try:
        data = request.json
        
        # Validation: Ensure all fields are provided
        required = ['name', 'company', 'year', 'kms_driven', 'fuel_type']
        if not all(k in data for k in required):
            return jsonify({"error": "Missing input fields"}), 400

        # Construct DataFrame for the model
        input_df = pd.DataFrame([[
            data['name'], 
            data['company'], 
            int(data['year']), 
            int(data['kms_driven']), 
            data['fuel_type']
        ]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
        
        # Predict
        prediction = model.predict(input_df)
        
        return jsonify({"price": round(float(prediction[0]), 2)})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)