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

    # 🧾 Show raw stock data
    st.dataframe(data)

    # 📊 7-Day Performance Summary
    st.markdown("### 📊 7-Day Performance Stats")
    price_change = data['Close'].iloc[-1] - data['Close'].iloc[0]
    percent_change = (price_change / data['Close'].iloc[0]) * 100
    st.write(f"Start Price: ${data['Close'].iloc[0]:.2f}")
    st.write(f"End Price:   ${data['Close'].iloc[-1]:.2f}")
    st.write(f"Change:      ${price_change:.2f} ({percent_change:.2f}%)")

    # 📉 Volatility
    volatility = data['Close'].std()
    st.write(f"📉 Volatility (std dev of closing prices): ${volatility:.2f}")

    # 🧠 GPT-style Summary (dummy response, since OpenAI API disabled)
    st.markdown("### 🧠 InsightBot Summary")
    st.write("📌 **Simulated GPT Summary**")
    st.info(f"""Over the past 7 days, {ticker.upper()} has shown a {'positive' if price_change > 0 else 'negative'} trend with a {percent_change:.2f}% {'increase' if price_change > 0 else 'decrease'} in closing price. Volatility remains moderate, indicating stable investor behavior.""")

    # 🧵 Bonus: Reddit Sentiment Summary (dummy data)
    st.markdown("### 💬 Reddit Sentiment Summary")
    sample_reddit_posts = [
        "🚀 $AAPL to the moon! Earnings crushed expectations!",
        "I'm concerned about $AAPL's declining iPhone sales...",
        "$AAPL stock is still a solid long-term hold. 🍎",
        "Big tech just keeps climbing. Holding my $AAPL shares tight.",
        "Could be time to take some profits on $AAPL."
    ]

    st.write("📢 Top Community Posts (simulated):")
    for post in sample_reddit_posts:
        st.write(f"- {post}")

    # 🧾 Simulated Sentiment Summary
    st.success("🧠 Community sentiment is **generally positive**, with investors showing optimism despite some concerns.")

