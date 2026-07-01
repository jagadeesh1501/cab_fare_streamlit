# 🚖 Cab Fare Prediction

A Machine Learning web application built with Streamlit that predicts cab fares based on pickup and dropoff GPS coordinates along with the number of passengers.

## 📌 Project Overview

This project uses a trained Machine Learning model to estimate cab fares using geographical coordinates and passenger count.

Users simply enter:

- Pickup Latitude
- Pickup Longitude
- Dropoff Latitude
- Dropoff Longitude
- Number of Passengers

and the application predicts the estimated cab fare instantly.

---

## ✨ Features

✔ Interactive Streamlit interface  
✔ Real-time fare prediction  
✔ GPS coordinate-based estimation  
✔ Passenger count selection slider  
✔ Clean dark-themed UI  
✔ Deployable on Streamlit Community Cloud

---

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Joblib

---

## 📂 Project Structure

```text
Cab_Fare_Prediction/
│
├── app.py
├── model.pkl
├── scaler.pkl
├── requirements.txt
├── README.md
└── dataset.csv
```

---

## 📊 Input Features

| Feature | Description |
|---------|-------------|
| Pickup Latitude | Starting point latitude |
| Pickup Longitude | Starting point longitude |
| Dropoff Latitude | Destination latitude |
| Dropoff Longitude | Destination longitude |
| Passenger Count | Number of passengers |

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Cab_Fare_Prediction.git
```

Move into the project folder

```bash
cd Cab_Fare_Prediction
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

## 📈 Model Information

The model was trained using cab trip data containing:

- Pickup Coordinates
- Dropoff Coordinates
- Passenger Count
- Fare Amount

Algorithms tested:

- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- XGBoost Regressor

The best-performing model was selected for deployment.

---

## 🎯 Example Input

```text
Pickup Latitude  : 40.7614
Pickup Longitude : -73.9776

Dropoff Latitude : 40.6413
Dropoff Longitude: -73.7781

Passengers       : 2
```

Predicted Fare:

```text
₹120.50
```

---

## 🌐 Deployment

This project can be deployed easily using:

- Streamlit Community Cloud
- Render
- Hugging Face Spaces

Deploy on Streamlit:

https://share.streamlit.io/

---

## 👨‍💻 Author

Jagadeesh

Machine Learning Project

Cab Fare Prediction using Streamlit
