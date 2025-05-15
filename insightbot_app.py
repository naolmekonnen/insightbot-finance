import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# ✅ Streamlit app layout and header
st.set_page_config(page_title="InsightBot Finance", layout="wide")
st.title("📈 InsightBot Finance Edition")
st.write("Analyze real-time stock trends with AI-powered summaries.")

# ✅ DEBUG BLOCK to confirm app is rendering
st.markdown("### ✅ App is running!")

# 🔍 Let user input a ticker
ticker = st.text_input("Enter stock ticker (e.g. AAPL, MSFT, TSLA)", value="AAPL")

if ticker:
    st.write(f"Fetching data for: {ticker}")

    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=7)

    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    data = data.reset_index()

    # 🧾 Show data table
    st.dataframe(data)

    # 📊 7-Day Performance Stats
    st.markdown("### 📊 7-Day Performance Stats")

    try:
        start_price = float(data['Close'].iloc[0])
        end_price = float(data['Close'].iloc[-1])
        price_change = end_price - start_price
        percent_change = (price_change / start_price) * 100

        st.write(f"Start Price: ${start_price:.2f}")
        st.write(f"End Price:   ${end_price:.2f}")
        st.write(f"Change:      ${price_change:.2f} ({percent_change:.2f}%)")
    except Exception as e:
        st.error("Error calculating price change.")
        st.exception(e)

    # 📉 BONUS: Volatility calculation
    try:
        volatility = float(data['Close'].std())
        st.write(f"📉 Volatility (std dev of closing prices): ${volatility:.2f}")
    except Exception as e:
        st.error("Error calculating volatility.")
        st.exception(e)
