import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import KFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
import pickle
import os

# Define absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, 'Cleaned_Car_data.csv')
model_path = os.path.join(BASE_DIR, 'LinearRegressionModel.pkl')

def train_and_validate():
    car = pd.read_csv(data_path)
    X = car[['name', 'company', 'year', 'kms_driven', 'fuel_type']]
    y = car['Price']

    # 1. Setup Pipeline with Gradient Boosting
    ohe = OneHotEncoder(handle_unknown='ignore')
    column_trans = make_column_transformer(
        (ohe, ['name', 'company', 'fuel_type']),
        remainder='passthrough'
    )
    
    # Gradient Boosting is much more powerful than Linear Regression
    gbr = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    pipe = make_pipeline(column_trans, gbr)

    # 2. N-Fold Cross Validation (K=5)
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(pipe, X, y, cv=kf, scoring='r2')

    print(f"✅ Cross-Validation Scores: {scores}")
    print(f"📊 Average R² Score: {np.mean(scores):.4f}")

    # 3. Final Training on the full dataset
    pipe.fit(X, y)

    # 4. Save the new model
    with open(model_path, 'wb') as f:
        pickle.dump(pipe, f)
    print(f"💾 Fresh Gradient Boosting model saved to {model_path}")

if __name__ == '__main__':
    train_and_validate()