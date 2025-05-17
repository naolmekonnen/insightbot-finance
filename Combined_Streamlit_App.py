
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import altair as alt
import requests
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import yfinance as yf

# App configuration
st.set_page_config(page_title="Finance & Crypto Insights", layout="wide")
st.title("Finance & Crypto Analysis Dashboard")

# Toggle selection for mode
selected_app = st.sidebar.radio("Choose App Mode", ["Stock InsightBot", "Crypto Dashboard"])

# -------------------- STOCK INSIGHTBOT -------------------- #
if selected_app == "Stock InsightBot":
    st.header("📈 Stock InsightBot")
    st.write("Analyze real-time stock trends with AI-powered summaries.")

    ticker = st.text_input("Enter stock ticker (e.g. AAPL, MSFT, TSLA)", value="AAPL")
    num_days = st.slider("Select number of days to analyze", min_value=5, max_value=30, value=7)

    @st.cache_data
    def fetch_data(ticker, start_date, end_date):
        return yf.download(ticker, start=start_date, end=end_date, progress=False).reset_index()

    if ticker:
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=num_days)

        with st.spinner("Fetching stock data..."):
            df = fetch_data(ticker, start_date, end_date)

        st.subheader(f"Price data for {ticker}")
        st.line_chart(df.set_index("Date")["Close"])
        st.dataframe(df)

# -------------------- CRYPTO DASHBOARD -------------------- #
elif selected_app == "Crypto Dashboard":
    st.header("💹 Cryptocurrency ML Dashboard")

    st.sidebar.header("API Configuration")
    api_key = st.sidebar.text_input("Enter CoinMarketCap API Key", type="password")
    fetch_data_btn = st.sidebar.button("Fetch Data")

    @st.cache_data
    def fetch_crypto_data(api_key, limit=50):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        parameters = {'start': '1', 'limit': str(limit), 'convert': 'USD'}
        headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        df = pd.json_normalize(data["data"])
        return df

    if fetch_data_btn and api_key:
        try:
            df = fetch_crypto_data(api_key)
            st.success("Data fetched successfully!")

            st.subheader("Top Cryptocurrencies")
            st.dataframe(df[["name", "symbol", "quote.USD.price", "quote.USD.volume_24h", "quote.USD.market_cap"]])

            # ML Example: Predicting price
            df["price"] = df["quote.USD.price"]
            df["volume_24h"] = df["quote.USD.volume_24h"]
            df["market_cap"] = df["quote.USD.market_cap"]

            X = df[["volume_24h", "market_cap"]]
            y = df["price"]

            scaler = MinMaxScaler()
            X_scaled = scaler.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)

            predictions = model.predict(X_test)

            st.subheader("Model Performance")
            st.write(f"R² Score: {r2_score(y_test, predictions):.2f}")
            st.write(f"MAE: {mean_absolute_error(y_test, predictions):.2f}")

            st.subheader("Predicted vs Actual Prices")
            pred_df = pd.DataFrame({"Actual": y_test.values, "Predicted": predictions})
            st.line_chart(pred_df.reset_index(drop=True))

        except Exception as e:
            st.error(f"Error fetching or processing data: {e}")
