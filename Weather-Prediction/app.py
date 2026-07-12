from flask import Flask, render_template, request
import joblib
import numpy as np
import time

app = Flask(__name__)

# Load the trained model
model = joblib.load('weather_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            start_time = time.time()
            
            # Get values from form
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            wind_speed = float(request.form['wind_speed'])
            pressure = float(request.form['pressure'])
            visibility = float(request.form['visibility'])
            
            # Prepare data for prediction
            features = np.array([[temperature, humidity, wind_speed, pressure, visibility]])
            
            # Predict and get probabilities
            prediction = model.predict(features)[0]
            probabilities = model.predict_proba(features)[0]
            confidence = max(probabilities) * 100
            
            end_time = time.time()
            prediction_time = round((end_time - start_time) * 1000, 2) # in ms
            
            result = {
                'prediction': prediction,
                'confidence': f"{confidence:.2f}%",
                'time': f"{prediction_time} ms",
                'inputs': {
                    'Temperature': f"{temperature} °C",
                    'Humidity': f"{humidity} %",
                    'Wind Speed': f"{wind_speed} km/h",
                    'Pressure': f"{pressure} hPa",
                    'Visibility': f"{visibility} km"
                }
            }
            
            return render_template('predict.html', result=result)
            
        except Exception as e:
            return render_template('predict.html', error=str(e))
            
    return render_template('predict.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
