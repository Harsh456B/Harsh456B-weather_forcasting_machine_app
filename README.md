# 🌦 Weather Forecasting Web App Using Machine Learning

## 🚀 Overview
This web app provides real-time weather forecasting using **machine learning**. It predicts temperature, humidity, and weather conditions by analyzing historical and real-time data. Built with **Streamlit**, it offers an intuitive UI for users to access predictions easily.

## ✨ Features
- 💽 Real-time weather data using **OpenWeatherMap API**
- 🔍 Machine learning-based predictions (Supervised & Unsupervised algorithms)
- 📊 Visualizations of temperature, humidity, and weather trends
- 🚀 Fast and lightweight UI built with **Streamlit**

## 🛠 Technologies Used
**Programming & Frameworks:** Python, Streamlit, FastAPI  
**Libraries:** Scikit-learn, Pandas, NumPy, Matplotlib  
**APIs & Deployment:** OpenWeatherMap API, Streamlit Sharing  
**Machine Learning Algorithms:** Supervised (Linear Regression, Random Forest, XGBoost), Unsupervised (K-Means Clustering)

## 🔬 Machine Learning Model
Our model utilizes **both supervised and unsupervised learning techniques**:
- **Supervised Learning:** Regression models predict numerical values like temperature and humidity.
- **Unsupervised Learning:** Clustering techniques analyze weather patterns and anomalies.

The model is trained on historical weather datasets and fine-tuned using real-time API data to improve accuracy. 

## ⚡ Challenges Faced & Solutions
### 🔴 Challenge: Slow model response time & inefficient API calls
✔ **Solution:** Optimized the model with quantization, improved preprocessing, and used **FastAPI** for faster request handling.

### 🔴 Challenge: Deployment issues on free-tier platforms
✔ **Solution:** Chose **Streamlit Sharing** for a lightweight, interactive UI with efficient hosting.

## 📌 Installation & Usage
1. **Clone the repository**:
   ```sh
   git clone https://github.com/yourusername/weather-forecasting-ml.git
   cd weather-forecasting-ml
   ```
2. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the Streamlit app**:
   ```sh
   streamlit run app.py
   ```

## 🎯 Future Enhancements
- Improve model accuracy with deep learning techniques
- Extend API support for multiple weather sources
- Enhance UI with interactive graphs & maps

## 🤝 Contributing
Contributions are welcome! Feel free to fork, create a branch, and submit a pull request.

## 🐜 License
This project is licensed under the **MIT License**.

---
Made with ❤️ by **Harsh Bhogal**
