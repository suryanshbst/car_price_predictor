import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import r2_score
import pickle
import os

# Define absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, 'Cleaned_Car_data.csv')
model_path = os.path.join(BASE_DIR, 'LinearRegressionModel.pkl')

def train_and_save_model():
    print("Loading cleaned dataset...")
    try:
        car = pd.read_csv(data_path)
    except FileNotFoundError:
        print("Error: Cleaned_Car_data.csv not found! Run clean_data.py first.")
        return

    # 1. Separate Features (X) and Target (y)
    X = car[['name', 'company', 'year', 'kms_driven', 'fuel_type']]
    y = car['Price']

    # 2. Train/Test Split (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=433)

    # 3. Handle Categorical Data (OneHotEncoding)
    ohe = OneHotEncoder()
    ohe.fit(X[['name', 'company', 'fuel_type']])

    column_trans = make_column_transformer(
        (OneHotEncoder(categories=ohe.categories_), ['name', 'company', 'fuel_type']),
        remainder='passthrough'
    )

    # 4. Initialize Linear Regression
    lr = LinearRegression()

    # 5. Create a Scikit-Learn Pipeline
    pipe = make_pipeline(column_trans, lr)

    print("Training the Linear Regression model...")
    pipe.fit(X_train, y_train)

    # 6. Evaluate the Model
    y_pred = pipe.predict(X_test)
    score = r2_score(y_test, y_pred)
    
    print("✅ Model trained successfully!")
    print(f"📊 R² Score: {score:.4f} (This means the model explains {score*100:.2f}% of the variance in car prices)")

    # 7. Save the Model
    with open(model_path, 'wb') as f:
        pickle.dump(pipe, f)
    print(f"💾 Fresh model saved to {model_path}")

if __name__ == '__main__':
    train_and_save_model()