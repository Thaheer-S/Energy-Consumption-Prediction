from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import requests
import matplotlib as plt

# Load models and scaler
scaler_path = 'scaler.pkl'
model_path = 'energy_predict.pkl'
data_path = 'Final_dataset.csv'
scaler = pickle.load(open(scaler_path, 'rb'))
model = pickle.load(open(model_path, 'rb'))
data = pd.read_csv(data_path)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')

@app.route('/analysis.html')
def analysis():
    return render_template('analysis.html')


@app.route('/predict.html',methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
        # Extract inputs in the exact order
            features = [
                float(request.form['Heat']),
                float(request.form['Pressure']),
                float(request.form['Humidity']),
                float(request.form['Temperature']),
                float(request.form['WindSpeed']),
                int(request.form['Weekend'])
            ]

        # Scale the input data
            scaled_features = scaler.transform([features])

        # Make prediction
            prediction = model.predict(scaled_features)
            predicted_kwh = prediction[0]

        # Calculate cost in rupees
            cost_per_kwh = 5  # 1 kWh = 5 Rs
            total_cost = predicted_kwh * cost_per_kwh

            return render_template(
                'predict.html',
                prediction_text=f"{predicted_kwh:.2f} kWh",
                cost_text=f"{total_cost:.2f} Rs"
            )
        except Exception as e:
            return render_template('predict.html', error_text=f"Error: {e}")

    return render_template('predict.html')

@app.route('/calculate_cost.html', methods=['GET', 'POST'])  # Allow both GET and POST methods
def calculate_cost():
    if request.method == 'POST':
        try:
            # Get the input value from the form
            kwh = float(request.form['kwh'])

            
            # Calculate the cost
            cost_per_kwh = 5  # Cost per kWh in Rs
            total_cost = kwh * cost_per_kwh
            
            # Return the calculated cost
            return render_template('calculate_cost.html', cost_text=f"Total Cost: ₹{total_cost:.2f}")
        except Exception as e:
            return render_template('calculate_cost.html', error_text=f"Error: {str(e)}")
    return render_template('calculate_cost.html')

# @app.route('/predict.html',methods=['POST'])
# def predict():
#     try:
#         # Extract inputs in the exact order
#         features = [
#             float(request.form['Heat']),
#             float(request.form['Pressure']),
#             float(request.form['Humidity']),
#             float(request.form['Temperature']),
#             float(request.form['WindSpeed']),
#             int(request.form['Weekend'])
#         ]

#         # Scale the input data
#         scaled_features = scaler.transform([features])

#         # Make prediction
#         prediction = model.predict(scaled_features)
#         predicted_kwh = prediction[0]

#         # Calculate cost in rupees
#         cost_per_kwh = 5  # 1 kWh = 5 Rs
#         total_cost = predicted_kwh * cost_per_kwh

#         return render_template(
#             'predict.html',
#             prediction_text=f"Predicted Energy Consumption: {predicted_kwh:.2f} kWh",
#             cost_text=f"Estimated Cost: {total_cost:.2f} Rs"
#         )
#     except Exception as e:
#         return render_template('predict.html', error_text=f"Error: {e}")

if __name__ == '__main__':
    app.run(debug=True)
