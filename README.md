# Stock Price Prediction using LSTM and Alpaca API

This project is designed to **demonstrate my fluency** with a variety of machine learning tools and libraries. Specifically, it combines **time series analysis**, **data preprocessing**, and a **Long Short-Term Memory (LSTM)** neural network to predict stock prices using historical market data.

---

## Overview

The code retrieves stock market data for a given ticker symbol (e.g., **AAPL**) using the **Alpaca API**. It preprocesses the data, prepares input sequences for modeling, and applies an LSTM neural network to forecast future stock prices. Finally, the predictions are visualized alongside actual prices to illustrate the model's performance.

The key steps include:

1. **Data Retrieval**: Using the Alpaca API to fetch historical stock data.  
2. **Preprocessing**: Scaling data and creating sequences for the LSTM model.  
3. **Modeling**: Training an LSTM network with TensorFlow/Keras.  
4. **Prediction**: Evaluating the model and visualizing predicted vs. actual prices.  

---

## Libraries Used

The following libraries are utilized to showcase a wide range of tools for data science and machine learning:

- **NumPy** and **Pandas**: For data manipulation and analysis.  
- **Alpaca API**: For accessing historical stock data.  
- **TensorFlow/Keras**: For building and training the LSTM neural network.  
- **Scikit-Learn**: For scaling and preprocessing data.  
- **Matplotlib**: For data visualization.  

---

## Code Walkthrough

1. **Data Loading**  
   - The Alpaca API fetches stock data within a specified date range.  
   - The data is filtered to include only the closing prices.

2. **Preprocessing**  
   - Data is normalized using `MinMaxScaler` to scale values between 0 and 1.  
   - A sliding window of size `60` is used to create input-output sequences for the LSTM model.

3. **Model Creation**  
   - An LSTM-based neural network is defined with:  
     - Input layer (`Input`)  
     - LSTM layer (`LSTM`)  
     - Dense output layer (`Dense`)  
   - The model is compiled using the `Adam` optimizer and `Mean Squared Error` loss.

4. **Training**  
   - The model is trained using the training dataset and validated on unseen test data.  
   - The trained model is saved to a file for future use.

5. **Prediction and Visualization**  
   - The model predicts prices on the test set.  
   - The predictions and actual prices are plotted using Matplotlib for comparison.

---

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.8+
- Required Python libraries (install via `pip`):
  ```bash
  pip install numpy pandas matplotlib scikit-learn tensorflow alpaca-trade-api
