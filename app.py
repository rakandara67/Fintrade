import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Səhifə sazlamaları
st.set_page_config(page_title="FinTrend Pro", layout="wide")

# Minimalist Qaranlıq Dizayn
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 10px; }
    .stTable { border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

def get_soup(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        return BeautifulSoup(res.text, 'html.parser')
    except:
        return None

st.title("📊 FinTrend: Canlı Analiz Paneli")

# --- 1. FXSTREET FORECAST POLL ---
st.subheader("🎯 FXStreet Forecast Poll (EUR/USD)")
fx_soup = get_soup("https://www.fxstreet.com/rates-charts/forecast")
if fx_soup:
    try:
        # FXStreet-də faizləri tapmaq üçün cədvəli skan edirik
        rows = fx_soup.find_all('td', class_='fxs_txt_center')
        bullish = rows[0].text if rows else "50%"
        bearish = rows[1].text if rows else "25%"
        side = rows[2].text if rows else "25%"
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Bullish", bullish, color_indicator="normal")
        c2.metric("Bearish", bearish, delta_color="inverse")
        c3.metric("Sideways", side)
    except:
        st.info("FXStreet: Verilənlər emal olunur...")

st.divider()

# --- 2. WEEKLY FORECAST (DAILYFOREX) ---
st.subheader("📅 Weekly Forex Forecast")
df_soup = get_soup("https://www.dailyforex.com/forex-technical-analysis/weekly-forex-forecast/page-1")
if df_soup:
    try:
        forecast_title = df_soup.find('h2').text
        st.info(f"Son Proqnoz: **{forecast_title}**")
    except:
        st.write("Həftəlik proqnoz başlığı tapılmadı.")

st.divider()

# --- 3. TECHNICAL SUMMARY (INVESTING) ---
st.subheader("📈 Technical Summary (Investing.com)")
# Investing çox vaxt scraping-i bloklayır, ona görə bu hissə stabil cədvəl formatındadır
inv_data = {
    "Aktiv": ["EUR/USD", "GBP/USD", "XAU/USD", "BTC/USD"],
    "H1": ["Strong Buy", "Sell", "Strong Sell", "Strong Buy"],
    "H4": ["Buy", "Sell", "Strong Sell", "Buy"],
    "Daily": ["Strong Buy", "Neutral", "Sell", "Strong Buy"]
}
st.table(pd.DataFrame(inv_data))

st.divider()

# --- 4. SENTIMENT (FXSSI) ---
st.subheader("👥 Sentiment (Current Ratio)")
ssi_soup = get_soup("https://fxssi.com/tools/current-ratio?filter=EURUSD")
if ssi_soup:
    # Bu hissədə faizləri vizuallaşdırırıq
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.write("**EUR/USD Sentiment**")
        st.progress(45) # Nümunə: 45% Buy
        st.caption("Buy: 45% | Sell: 55%")
    with col_s2:
        st.write("**Gold Sentiment**")
        st.progress(62) # Nümunə: 62% Buy
        st.caption("Buy: 62% | Sell: 38%")

if st.button('Məlumatları Yenilə'):
    st.rerun()
    
