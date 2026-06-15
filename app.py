import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Stock Market Dashboard")
st.write("View historical stock market data with interactive charts.")

# Sidebar
st.sidebar.header("Settings")

ticker = st.sidebar.text_input(
    "Enter Stock Symbol",
    value="AAPL"
).upper()

period = st.sidebar.selectbox(
    "Select Time Period",
    ["1mo", "3mo", "6mo", "1y", "2y", "5y"]
)

# Download Data
try:
    data = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    if data.empty:
        st.error("No data found. Please check the stock symbol.")
    else:
        st.subheader(f"{ticker} Historical Data")
        st.dataframe(data)

        # Close Price Chart
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                mode="lines",
                name="Close Price"
            )
        )

        fig.update_layout(
            title=f"{ticker} Closing Price",
            xaxis_title="Date",
            yaxis_title="Price",
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        # Moving Average
        data["20 Day MA"] = data["Close"].rolling(20).mean()

        ma_fig = go.Figure()

        ma_fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                name="Close Price"
            )
        )

        ma_fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["20 Day MA"],
                name="20 Day Moving Average"
            )
        )

        ma_fig.update_layout(
            title="Closing Price vs 20-Day Moving Average",
            height=500
        )

        st.plotly_chart(ma_fig, use_container_width=True)

        # Download CSV
        csv = data.to_csv().encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"{ticker}_stock_data.csv",
            mime="text/csv"
        )

except Exception as e:
    st.error(f"Error: {e}")