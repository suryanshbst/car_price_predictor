import pandas as pd
import tensorflow as tf
from tensorflow.keras import layers
import os

# Go up one level to reach 'ml_service' and then point directly to the file
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'Cleaned_Car_data.csv')

def build_and_train():
    # 1. Load the data
    df = pd.read_csv(DATA_PATH)
    
    # 2. Prepare the numeric features
    X = df[['year', 'kms_driven']].values 
    y = df['Price'].values

    # 3. Define the Neural Network architecture
    model = tf.keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=(2,)), 
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])

    # 4. Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # 5. Train the model (Backpropagation happens here)
    print("🚀 Training Neural Network...")
    model.fit(X, y, epochs=50, batch_size=32, verbose=1)
    
    print("✅ Training complete.")

if __name__ == '__main__':
    build_and_train()