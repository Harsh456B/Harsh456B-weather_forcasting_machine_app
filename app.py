import streamlit as st
import requests
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta
import pytz

# Custom CSS for motion effects and animations
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;git branch -M main
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        padding: 10px 24px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        transform: scale(1);
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.12);
        transform: scale(1.1);
    }
    .stTextInput>div>div>input {
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #ccc;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .weather-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.12);
    }
    .weather-icon {
        width: 50px;
        height: 50px;
        margin-bottom: 10px;
        transition: transform 0.3s ease;
    }
    .weather-icon:hover {
        transform: rotate(360deg);
    }
    .dashboard {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    .dashboard-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        flex: 1 1 calc(33.333% - 40px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .dashboard-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15), 0 3px 6px rgba(0, 0, 0, 0.12);
    }
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Weather Icons (You can replace these with actual image URLs or local files)
WEATHER_ICONS = {
    "clear": "https://cdn-icons-png.flaticon.com/512/6974/6974833.png",
    "clouds": "https://cdn-icons-png.flaticon.com/512/1146/1146869.png",
    "rain": "https://cdn-icons-png.flaticon.com/512/1163/1163624.png",
    "thunderstorm": "https://cdn-icons-png.flaticon.com/512/992/992915.png",
    "snow": "https://cdn-icons-png.flaticon.com/512/2315/2315309.png",
    "mist": "https://cdn-icons-png.flaticon.com/512/1779/1779940.png",
    "default": "https://cdn-icons-png.flaticon.com/512/869/869869.png"
}

API_KEY = 'c5385722edf9ea23965d802ab9842e35'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'

# Function to get current weather data
def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        weather_condition = data['weather'][0]['main'].lower()
        icon_url = WEATHER_ICONS.get(weather_condition, WEATHER_ICONS['default'])
        return {
            'city': data.get('name', 'Unknown City'),
            'country': data['sys'].get('country', 'Unknown'),
            'current_temp': round(data['main'].get('temp', 0)),
            'feels_like': round(data['main'].get('feels_like', 0)),
            'temp_min': round(data['main'].get('temp_min', 0)),
            'temp_max': round(data['main'].get('temp_max', 0)),
            'humidity': round(data['main'].get('humidity', 0)),
            'description': data['weather'][0].get('description', 'No description'),
            'wind_speed': data['wind'].get('speed', 0),
            'pressure': data['main'].get('pressure', 0),
            'rain': 'Yes' if 'rain' in data else 'No',
            'icon': icon_url
        }
    else:
        st.error(f"Error fetching weather data: {data.get('message', 'Unknown error')}")
        return None

# Function to get 5 days weather forecast data
def get_5_day_forecast(city):
    url = f"{BASE_URL}forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    
    if response.status_code == 200:
        forecast = []
        for entry in data['list']:
            forecast.append({
                'time': entry['dt_txt'],
                'temp': round(entry['main']['temp']),
                'humidity': round(entry['main']['humidity']),
                'weather': entry['weather'][0]['main'].lower(),
                'icon': WEATHER_ICONS.get(entry['weather'][0]['main'].lower(), WEATHER_ICONS['default'])
            })
        return forecast
    else:
        st.error(f"Error fetching forecast data: {data.get('message', 'Unknown error')}")
        return []

# Function to prepare data for regression (X and Y for features and target)
def prepare_regression_data(df, target_column):
    df['Time'] = pd.to_datetime(df['Time'])
    df['Hour'] = df['Time'].dt.hour  # Extracting the hour from the timestamp as a featuregit branch -M main
    y = df[target_column]  # Target is the column we want to predict, e.g., 'Temp'

    return X, y

# Function to train the regression model
def train_regression_model(X, y):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# Function to predict future values
def predict_future(model, last_value):
    # We will predict based on the last value, but you may improve the model logic for time-based prediction
    future_predictions = []
    for _ in range(5):
        future_predictions.append(last_value)  # Dummy prediction logic, modify as needed
    return future_predictions

# Streamlit UI
st.title('🌤️ Weather Forecasting App')

data_source = st.radio("Choose Data Source:", ("Live Weather Data", "Upload Historical Data"))

timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.now(timezone)
st.write(f"📅 **Date:** {current_time.strftime('%Y-%m-%d')} 🕒 **Time:** {current_time.strftime('%H:%M')} IST")

if data_source == "Live Weather Data":
    city = st.text_input("Enter City Name")
    if city:
        current_weather = get_current_weather(city)
        if current_weather:
            st.markdown(f"""
                <div class="weather-card">
                    <img src="{current_weather['icon']}" class="weather-icon">
                    <h3>🌍 {current_weather['city']}, {current_weather['country']}</h3>
                    <p>🌡️ <b>Current Temperature:</b> {current_weather['current_temp']}°C</p>
                    <p>🌡️ <b>Feels Like:</b> {current_weather['feels_like']}°C</p>
                    <p>🌡️ <b>Min Temperature:</b> {current_weather['temp_min']}°C</p>
                    <p>🌡️ <b>Max Temperature:</b> {current_weather['temp_max']}°C</p>
                    <p>💧 <b>Humidity:</b> {current_weather['humidity']}%</p>
                    <p>🌦️ <b>Weather Description:</b> {current_weather['description']}</p>
                    <p>☔ <b>Rain Prediction:</b> {current_weather['rain']}</p>
                </div>
            """, unsafe_allow_html=True)

        # Get and display 5 days weather forecast
        forecast = get_5_day_forecast(city)
        if forecast:
            st.markdown("""
                <div class="weather-card">
                    <h3 style="text-align: center; font-size: 24px; font-weight: bold; color: #FFD700; animation: bounce 1s ease infinite;">
                        FUTURE WEATHER FORECASTING
                    </h3>
                </div>
            """, unsafe_allow_html=True)
            for entry in forecast:
                st.markdown(f"""
                    <div class="weather-card">
                        <img src="{entry['icon']}" class="weather-icon">
                        <h4>🕒 {entry['time']}</h4>
                        <p>🌡️ <b>Temperature:</b> {entry['temp']}°C</p>
                        <p>💧 <b>Humidity:</b> {entry['humidity']}%</p>
                        <p>🌦️ <b>Weather:</b> {entry['weather'].capitalize()}</p>
                    </div>
                """, unsafe_allow_html=True)

elif data_source == "Upload Historical Data":
    uploaded_file = st.file_uploader("📂 Upload Historical Weather Data (CSV)", type="csv")
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.dropna(inplace=True)
        df.drop_duplicates(inplace=True)
        st.write("✅ **Data Uploaded Successfully!**")
        st.dataframe(df.head())
        
        city = st.text_input("🏙️ Enter City Name for Prediction")
        
        if city:
            st.write(f"🔍 Predicting weather for **{city}** using uploaded historical data...")
            
            # Train models
            x_temp, y_temp = prepare_regression_data(df, 'Temp')
            x_hum, y_hum = prepare_regression_data(df, 'Humidity')
            temp_model = train_regression_model(x_temp, y_temp)
            hum_model = train_regression_model(x_hum, y_hum)
            
            # Predict future temperature & humidity
            future_temp = predict_future(temp_model, df['Temp'].iloc[-1])
            future_humidity = predict_future(hum_model, df['Humidity'].iloc[-1])
            
            # Generate future timestamps
            next_hour = current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            future_times = [(next_hour + timedelta(hours=i)).strftime("%H:%M") for i in range(5)]
            
            # Display predictions in a dashboard format
            st.markdown("""<div class="dashboard">""", unsafe_allow_html=True)
            for time, temp in zip(future_times, future_temp):
                st.markdown(f"<div class='dashboard-card'><h3>🕒 {time}</h3><p>Temperature: {round(temp, 1)}°C</p></div>", unsafe_allow_html=True)
            for time, humidity in zip(future_times, future_humidity):
                st.markdown(f"<div class='dashboard-card'><h3>🕒 {time}</h3><p>Humidity: {round(humidity, 1)}%</p></div>", unsafe_allow_html=True)
            st.markdown("""</div>""", unsafe_allow_html=True)
