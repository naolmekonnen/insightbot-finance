
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import requests
import json
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

st.set_page_config(page_title="Cryptocurrency ML Analysis Dashboard", layout="wide")
st.title("Cryptocurrency Analysis and ML Insights")

# Sidebar API input
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter CoinMarketCap API Key", type="password")
fetch_data = st.sidebar.button("Fetch Data")

@st.cache_data
def fetch_crypto_data(api_key, limit=50):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': '1', 'limit': str(limit), 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': api_key}
    response = requests.get(url, params=parameters, headers=headers)
    data = json.loads(response.text)
    df = pd.json_normalize(data['data'])
    df['timestamp'] = pd.to_datetime('now')
    df.columns = df.columns.str.replace(".", "_")
    return df

if fetch_data and api_key:
    df = fetch_crypto_data(api_key)
    st.session_state['crypto_df'] = df
    st.success("Data retrieved successfully")

if 'crypto_df' in st.session_state:
    df = st.session_state['crypto_df']
    st.subheader("Raw Data Snapshot")
    st.dataframe(df.head(20))

    st.subheader("Top Coins by Market Cap")
    top_coins = df.sort_values(by="quote_USD_market_cap", ascending=False).head(10)
    st.bar_chart(top_coins.set_index("name")["quote_USD_market_cap"])

    st.subheader("Volume vs Price Scatterplot")
    scatter = alt.Chart(df).mark_circle(size=60).encode(
        x="quote_USD_volume_24h", y="quote_USD_price", color="name",
        tooltip=["name", "quote_USD_price", "quote_USD_volume_24h"]
    ).interactive()
    st.altair_chart(scatter, use_container_width=True)

    st.subheader("Feature Engineering Outputs")
    df["price_change"] = df["quote_USD_percent_change_24h"]
    df["z_score"] = (df["price_change"] - df["price_change"].mean()) / df["price_change"].std()
    st.write("Price Change and Z-score Added")
    st.dataframe(df[["name", "quote_USD_price", "price_change", "z_score"]].head(10))

    st.subheader("Anomaly Detection Based on Z-score")
    anomalies = df[df["z_score"].abs() > 2]
    st.write("Detected Anomalies (z-score > 2 or < -2)")
    st.dataframe(anomalies[["name", "quote_USD_price", "price_change", "z_score"]])

    st.subheader("Similarity Recommendation Engine")
    feature_cols = ["quote_USD_price", "quote_USD_volume_24h", "quote_USD_market_cap"]
    df_clean = df.dropna(subset=feature_cols).copy()
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(df_clean[feature_cols])
    sim_matrix = cosine_similarity(scaled_features)
    selected_coin = st.selectbox("Select a Coin", df_clean["name"])
    if selected_coin:
        idx = df_clean[df_clean["name"] == selected_coin].index[0]
        scores = list(enumerate(sim_matrix[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        st.write("Top 5 Similar Coins:")
        for i, score in scores[1:6]:
            st.write(f"{df_clean.iloc[i]['name']}: Similarity Score = {round(score, 4)}")

 

    st.subheader("Market Cap Prediction (Random Forest Regression)")
    X = scaled_features
    y = df_clean["quote_USD_market_cap"].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    st.write(f"Model R² Score: {r2_score(y_test, y_pred):.4f}")
    st.write(f"Mean Absolute Error: ${mean_absolute_error(y_test, y_pred):,.0f}")

    st.subheader("Interactive Market Cap Prediction")
    price_input = st.slider("Select Price", 0.01, float(df["quote_USD_price"].max()), float(df["quote_USD_price"].mean()))
    volume_input = st.slider("Select Volume (24h)", 0.01, float(df["quote_USD_volume_24h"].max()), float(df["quote_USD_volume_24h"].mean()))
    cap_input = 0
    user_scaled = scaler.transform([[price_input, volume_input, cap_input]])
    prediction = rf.predict(user_scaled)[0]
    st.write(f"Predicted Market Cap: ${prediction:,.0f}")

else:
    st.info("Please enter your API key and fetch the data to begin.")
