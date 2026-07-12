import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    
    # Temperature: 0 to 40 C
    # Humidity: 20 to 100 %
    # Wind Speed: 0 to 50 km/h
    # Pressure: 980 to 1030 hPa
    # Visibility: 0 to 20 km
    
    temp = np.random.uniform(0, 40, num_samples)
    humidity = np.random.uniform(20, 100, num_samples)
    wind_speed = np.random.uniform(0, 50, num_samples)
    pressure = np.random.uniform(980, 1030, num_samples)
    visibility = np.random.uniform(0, 20, num_samples)
    
    # Logic to generate realistic weather labels based on conditions
    weather = []
    for t, h, w, p, v in zip(temp, humidity, wind_speed, pressure, visibility):
        if p < 1000 and h > 80 and w > 30:
            weather.append('Stormy ⛈️')
        elif p < 1010 and h > 70:
            weather.append('Rainy 🌧️')
        elif h > 60 or (t < 20 and v < 5):
            weather.append('Cloudy ☁️')
        else:
            weather.append('Sunny ☀️')
            
    df = pd.DataFrame({
        'Temperature': temp,
        'Humidity': humidity,
        'Wind_Speed': wind_speed,
        'Pressure': pressure,
        'Visibility': visibility,
        'Weather': weather
    })
    
    return df

def main():
    print("Generating synthetic dataset...")
    df = generate_synthetic_data(1500)
    
    # Ensure dataset directory exists
    os.makedirs('dataset', exist_ok=True)
    
    # Save dataset
    dataset_path = 'dataset/weather.csv'
    df.to_csv(dataset_path, index=False)
    print(f"Dataset saved to {dataset_path}")
    
    # Prepare data for training
    X = df[['Temperature', 'Humidity', 'Wind_Speed', 'Pressure', 'Visibility']]
    y = df['Weather']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    print(f"Model trained! Accuracy on test set: {accuracy:.2f}")
    
    # Save the model
    model_path = 'weather_model.pkl'
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    main()
