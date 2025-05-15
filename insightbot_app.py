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
    
    st.dataframe(data)  # Show data table
