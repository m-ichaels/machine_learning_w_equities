import numpy as np
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.enums import Adjustment
from alpaca.data.enums import DataFeed
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import datetime
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

def load_stock_data(ticker, start_date, end_date, timeframe=TimeFrame.Day):
    request_params = StockBarsRequest(
        symbol_or_symbols=[ticker],
        timeframe=timeframe,
        start=start_date,
        end=end_date,
        adjustment=Adjustment.RAW,
        feed=DataFeed.IEX
    )
    bars = client.get_stock_bars(request_params)

    print("DataFrame Structure:")
    print(bars.df.head())

    try:
        data = bars.df.xs(ticker, level="symbol")
        print(f"Extracted data for {ticker}:")
        print(data.head())
        return data[['close']]
    except KeyError as e:
        print(f"No data found for {ticker}. Check the ticker and API response.")
        return pd.DataFrame()

ticker = "AAPL"
start_date = (datetime.datetime.now() - datetime.timedelta(days=365)).isoformat()
end_date = datetime.datetime.now().isoformat()

stock_data = load_stock_data(ticker, start_date, end_date)
stock_data = stock_data.reset_index()
print(stock_data.head())

scaler = MinMaxScaler(feature_range=(0, 1))
prices = scaler.fit_transform(stock_data['close'].values.reshape(-1, 1))

window_size = 60

def create_sequences(data, window_size):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size])
    return np.array(X), np.array(y)

X, y = create_sequences(prices, window_size)

split_idx = int(0.8 * len(X))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

input_sequence = Input(shape=(window_size, 1), name='input_sequence')
lstm = LSTM(50, return_sequences=False, name='lstm_layer')(input_sequence)
dense_out = Dense(1, activation='linear', name='output_layer')(lstm)

model = Model(inputs=input_sequence, outputs=dense_out)
model.compile(optimizer='adam', loss='mean_squared_error')

model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=20,
    batch_size=32,
    verbose=1
)

model.save('./stock_forecasting_model.keras')

predicted_prices = model.predict(X_test)
predicted_prices = scaler.inverse_transform(predicted_prices)
actual_prices = scaler.inverse_transform(y_test.reshape(-1, 1))

plt.figure(figsize=(10, 6))
plt.plot(actual_prices, label="Actual Prices", color="blue")
plt.plot(predicted_prices, label="Predicted Prices", color="red")
plt.title(f"{ticker} Stock Price Prediction")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
