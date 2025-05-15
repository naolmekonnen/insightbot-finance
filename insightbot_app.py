import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Streamlit app layout and header
st.set_page_config(page_title="InsightBot Finance", layout="wide")
st.title("InsightBot Finance Edition")
st.write("Analyze real-time stock trends with AI-powered summaries.")

# Debug block to confirm app is rendering
st.markdown("### App is running!")

# Let user input a ticker
ticker = st.text_input("Enter stock ticker (e.g. AAPL, MSFT, TSLA)", value="AAPL")

# Cache stock data fetch
@st.cache_data
def fetch_data(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date, progress=False).reset_index()

if ticker:
    st.write(f"Fetching data for: {ticker}")

    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=7)

    # Add loading spinner while fetching
    with st.spinner("Fetching stock data..."):
        data = fetch_data(ticker, start_date, end_date)

    # Show raw data
    st.dataframe(data)

    # 📈 Chart of closing prices
    st.line_chart(data['Close'])

    # Performance metrics section
    st.markdown("## 7-Day Performance Stats")

    try:
        start_price = float(data['Close'].iloc[0])
        end_price = float(data['Close'].iloc[-1])
        price_change = end_price - start_price
        percent_change = (price_change / start_price) * 100
        volatility = float(data['Close'].std())

        st.write(f"Start Price: ${start_price:.2f}")
        st.write(f"End Price:   ${end_price:.2f}")
        st.write(f"Change:      ${price_change:.2f} ({percent_change:.2f}%)")
        st.write(f"Volatility (std dev of closing prices): ${volatility:.2f}")

    except Exception as e:
        st.error("Error calculating performance statistics.")
        st.exception(e)

# Simulated Reddit Sentiment Summary
st.markdown("## Reddit Sentiment Summary (Simulated)")

dummy_posts = [
    "Just bought more AAPL. Long-term hold!",
    "Worried about the dip, but holding steady.",
    "AAPL earnings were solid. Thinking bullish.",
    "Sell-off was an overreaction IMO.",
    "I’m buying every dip this month!"
]

positive = [p for p in dummy_posts if "bullish" in p or "buying" in p or "hold" in p]
negative = [p for p in dummy_posts if "worried" in p or "sell-off" in p]

st.write("Posts Analyzed:", len(dummy_posts))
st.write("Positive Mentions:", len(positive))
st.write("Negative Mentions:", len(negative))

with st.expander("View Sample Reddit Posts"):
    for post in dummy_posts:
        st.markdown(f"- {post}")

# GitHub link footer
st.markdown("---")
st.markdown("View the code on [GitHub](https://github.com/naolmekonnen/insightbot-finance)")
