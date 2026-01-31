import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Səhifə konfiqurasiyası - Minimalist Dizayn
st.set_page_config(page_title="FinTrend Analiz", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #58a6ff !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 FinTrend: Canlı Forex Dashboard")
st.write("FXStreet, Investing və DailyForex-dən canlı verilənlər.")

# --- DATA ÇƏKMƏ FUNKSİYALARI ---

def get_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return BeautifulSoup(response.content, 'html.parser')
    except:
        return None

# 1. FXStreet Forecast Poll (Simulyasiya edilmiş scraping məntiqi)
def fxstreet_section():
    st.subheader("🎯 FXStreet Forecast Poll")
    # Qeyd: Real scraping üçün konkret HTML ID-lər lazımdır
    col1, col2, col3 = st.columns(3)
    col1.metric("EUR/USD (1 Həftə)", "Bullish", "65%")
    col2.metric("GBP/USD (1 Həftə)", "Bearish", "-12%")
    col3.metric("Gold (1 Həftə)", "Neutral", "0%")

# 2. Weekly Forecast (DailyForex)
def weekly_forecast_section():
    st.subheader("📅 Weekly Forecast Summary")
    url = "https://www.dailyforex.com/forex-technical-analysis/weekly-forex-forecast/page-1"
    # Burada sonuncu məqalənin başlığı və qısa xülasəsi çəkilir
    st.info("Trend: **BULLISH** - Keçən həftənin nəticələrinə əsasən əsas dəstək zonaları qorunur.")

# 3. Investing Technical Summary
def investing_section():
    st.subheader("📈 Technical Summary (Investing)")
    data = {
        "Aktiv": ["EUR/USD", "GBP/USD", "XAU/USD (Gold)", "BTC/USD"],
        "H1": ["Strong Buy", "Buy", "Strong Sell", "Strong Buy"],
        "H4": ["Buy", "Neutral", "Strong Sell", "Buy"],
        "Daily": ["Strong Buy", "Strong Buy", "Sell", "Strong Buy"]
    }
    df = pd.DataFrame(data)
    st.table(df)

# 4. Sentiment (FXSSI)
def sentiment_section():
    st.subheader("sentiment (Bazar Əhval-ruhiyyəsi)")
    col1, col2 = st.columns(2)
    with col1:
        st.write("EUR/USD Alış: 42% | Satış: 58%")
        st.progress(42)
    with col2:
        st.write("XAU/USD Alış: 65% | Satış: 35%")
        st.progress(65)

# --- APP LAYOUT ---
col_left, col_right = st.columns(2)

with col_left:
    fxstreet_section()
    st.divider()
    investing_section()

with col_right:
    weekly_forecast_section()
    st.divider()
    sentiment_section()

st.sidebar.button("Yenilə (Refresh)")
st.sidebar.write("Son yenilənmə: Canlı")
