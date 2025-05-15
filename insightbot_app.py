import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# ✅ Streamlit app layout and header
st.set_page_config(page_title="InsightBot Finance", layout="wide")
st.title("📈 InsightBot Finance Edition")
st.write("Analyze real-time stock trends with AI-powered summaries.")
