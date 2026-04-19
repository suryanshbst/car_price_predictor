import pandas as pd
import os

# Define the absolute paths so it always finds the right folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raw_data_path = os.path.join(BASE_DIR, 'quikr_car.csv')
cleaned_data_path = os.path.join(BASE_DIR, 'Cleaned_Car_data.csv')

def clean_dataset():
    print(f"Loading raw dataset from {raw_data_path}...")
    try:
        car = pd.read_csv(raw_data_path)
    except FileNotFoundError:
        print("Error: 'quikr_car.csv' not found! Please ensure it is in the ml_service folder.")
        return

    print("Cleaning 'year' column...")
    car = car[car['year'].str.isnumeric()]
    car['year'] = car['year'].astype(int)

    print("Cleaning 'Price' column...")
    car = car[car['Price'] != 'Ask For Price']
    car['Price'] = car['Price'].str.replace(',', '').astype(int)

    print("Cleaning 'kms_driven' column...")
    car['kms_driven'] = car['kms_driven'].str.split().str.get(0).str.replace(',', '')
    car = car[car['kms_driven'].str.isnumeric()]
    car['kms_driven'] = car['kms_driven'].astype(int)

    print("Cleaning 'fuel_type' column...")
    car = car[~car['fuel_type'].isna()]

    print("Standardizing 'name' column (keeping first 3 words)...")
    car['name'] = car['name'].str.split().str.slice(start=0, stop=3).str.join(' ')

    print("Removing extreme outliers (Prices > 6,000,000)...")
    car = car[car['Price'] < 6000000]

    # Reset index for a clean dataframe
    car = car.reset_index(drop=True)

    print(f"Saving cleaned dataset to {cleaned_data_path}...")
    # index=False prevents pandas from writing the row numbers as a new column
    car.to_csv(cleaned_data_path, index=False)
    
    print("✅ Dataset cleaned and saved successfully!")
    print(f"Final shape of data: {car.shape}")

if __name__ == '__main__':
    clean_dataset()