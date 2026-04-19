from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# This tells Python: "Find the exact folder this app.py file is sitting in"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths securely
model_path = os.path.join(BASE_DIR, 'LinearRegressionModel.pkl')
data_path = os.path.join(BASE_DIR, 'Cleaned_Car_data.csv')

# Load the files using the secure paths
try:
    model = pickle.load(open(model_path, 'rb'))
    car_data = pd.read_csv(data_path)
    print("✅ Model and Data loaded successfully!")
except Exception as e:
    print(f"❌ Error loading files: {e}")

@app.route('/api/options', methods=['GET'])
def get_options():
    # Group models by company
    company_model_map = car_data.groupby('company')['name'].unique().apply(list).to_dict()
    
    return jsonify({
        "companies": sorted(car_data['company'].unique().tolist()),
        "company_model_map": company_model_map, # This is the key!
        "years": sorted(car_data['year'].unique().tolist(), reverse=True),
        "fuel_types": car_data['fuel_type'].dropna().unique().tolist()
    })
    
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # 1. Validation: Ensure required fields are not empty
        required_fields = ['name', 'company', 'year', 'kms_driven', 'fuel_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"error": f"Missing or empty field: {field}"}), 400

        # 2. Format incoming JSON into a DataFrame
        prediction_df = pd.DataFrame(columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
        
        # 3. Safely convert to correct types
        prediction_df.loc[0] = [
            data.get('name'), 
            data.get('company'), 
            int(data.get('year')), 
            int(data.get('kms_driven')), 
            data.get('fuel_type')
        ]
        
        # 4. Predict
        prediction = model.predict(prediction_df)
        
        # 5. Return JSON
        return jsonify({"price": round(prediction[0], 2)})
        
    except ValueError as ve:
        # Specifically catch conversion errors (like trying to turn '' into an int)
        return jsonify({"error": f"Invalid data format: {str(ve)}"}), 400
    except Exception as e:
        # Catch unexpected errors
        print(f"Server error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on port 5000
    app.run(port=5000, debug=True)