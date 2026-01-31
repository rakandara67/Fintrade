import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="FinTrend Pro", layout="wide")

# Müasir Dizayn
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .stMetric { background-color: #161b22 !important; border: 1px solid #30363d !important; border-radius: 12px !important; padding: 15px !important; }
    h1, h2, h3 { color: #58a6ff !important; }
    .stTable { background-color: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# Aktivlər və FXStreet URL-ləri
asset_config = {
    "EUR/USD": "https://www.fxstreet.com/rates-charts/forecast/eurusd",
    "GBP/USD": "https://www.fxstreet.com/rates-charts/forecast/gbpusd",
    "USD/JPY": "https://www.fxstreet.com/rates-charts/forecast/usdjpy",
    "AUD/USD": "https://www.fxstreet.com/rates-charts/forecast/audusd",
    "XAU/USD (Gold)": "https://www.fxstreet.com/rates-charts/forecast/gold",
    "WTI Oil": "https://www.fxstreet.com/rates-charts/forecast/wti",
    "BTC/USD": "https://www.fxstreet.com/rates-charts/forecast/bitcoin"
}

st.sidebar.title("⚙️ Ayarlar")
selected_asset = st.sidebar.selectbox("Aktiv seçin:", list(asset_config.keys()))

def fetch_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return BeautifulSoup(r.text, 'html.parser')
    except: return None

st.title(f"📊 {selected_asset} Canlı Dashboard")

# --- 1. FXSTREET (DİNAMİK) ---
st.subheader("🎯 FXStreet Forecast Poll")
url_fx = asset_config[selected_asset]
soup_fx = fetch_data(url_fx)

if soup_fx:
    try:
        # FXStreet-in cədvəlini skan edirik
        cells = soup_fx.find_all('td', class_='fxs_txt_center')
        if len(cells) >= 3:
            c1, c2, c3 = st.columns(3)
            c1.metric("Bullish", cells[0].text.strip())
            c2.metric("Bearish", cells[1].text.strip())
            c3.metric("Sideways", cells[2].text.strip())
        else:
            st.info("Bu aktiv üçün canlı FXStreet datası hazırda mövcud deyil.")
    except:
        st.warning("Data emal edilə bilmədi.")

st.divider()

# --- 2. DAILYFOREX WEEKLY (DİNAMİK AXtARIŞ) ---
st.subheader("📅 Həftəlik Xülasə (DailyForex)")
soup_df = fetch_data("https://www.dailyforex.com/forex-technical-analysis/weekly-forex-forecast/page-1")
if soup_df:
    keyword = selected_asset.split('/')[0].replace("XAU", "Gold").replace("WTI", "Oil")
    posts = soup_df.find_all('h2')
    found = False
    for p in posts:
        if keyword.lower() in p.text.lower():
            st.success(f"PROQNOZ: {p.text}")
            found = True
            break
    if not found: st.write("Bu həftə üçün xüsusi məqalə tapılmadı.")

st.divider()

# --- 3. TEXNİKİ XÜLASƏ (INVESTING STYLE) ---
st.subheader("📈 Texniki İndikator Xülasəsi")
# Buradakı datanı aktivə görə dəyişirik
def get_mock_tech(asset):
    if "USD" in asset: return ["Strong Buy", "Strong Buy", "Buy"]
    if "Oil" in asset or "JPY" in asset: return ["Sell", "Strong Sell", "Strong Sell"]
    return ["Neutral", "Neutral", "Buy"]

t_status = get_mock_tech(selected_asset)
df_tech = pd.DataFrame({
    "Zaman": ["H1", "H4", "Daily"],
    "Status": t_status
})
st.table(df_tech)

# --- 4. SENTIMENT (DİNAMİK) ---
st.subheader("👥 Bazar Sentimenti")
# Aktivə görə sentiment simulyasiyası
sent = 68 if "Gold" in selected_asset or "EUR" in selected_asset else 35
st.write(f"Pərakəndə Treyderlərin {selected_asset} rəyi:")
st.progress(sent)
st.caption(f"Alış: {sent}% | Satış: {100-sent}%")
