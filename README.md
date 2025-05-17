# Cryptocurrency Streamlit Dashboard

This Streamlit app allows users to:
- Fetch live cryptocurrency data using the CoinMarketCap API
- Visualize top coins by market cap and volume/price patterns
- Detect anomalies using z-score on price changes
- Generate similar coin recommendations based on cosine similarity
- Perform regression prediction of market cap using Random Forest
- Explore data interactively through filters and sliders

## How to Run Locally

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the Streamlit app:
```
streamlit run Final_Complete_Crypto_Streamlit_App.py
```

3. Enter your CoinMarketCap API key in the sidebar to begin.

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to https://streamlit.io/cloud and deploy using this script
