import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import os

# Go up one level from 'research' to reach the CSV in 'ml_service'
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Cleaned_Car_data.csv')

def build_scratch_model():
    # Load and prepare data
    df = pd.read_csv(DATA_PATH)
    # Simple selection for demonstration: use only numeric columns for the "from scratch" model
    # (Handling strings requires OneHotEncoding which we keep in the production GBR model)
    X = df[['year', 'kms_driven']].values
    y = df['Price'].values

    # Build the Neural Network
    model = Sequential([
        Dense(64, activation='relu', input_shape=(2,)),
        Dense(32, activation='relu'),
        Dense(1) # Linear output for regression
    ])

    model.compile(optimizer='adam', loss='mse')

    # Train
    print("🚀 Training Neural Network...")
    model.fit(X, y, epochs=50, batch_size=32, verbose=1)
    
    print("✅ Model trained from scratch.")

if __name__ == '__main__':
    build_scratch_model()