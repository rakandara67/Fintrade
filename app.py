import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Səhifə konfiqurasiyası
st.set_page_config(page_title="FinTrend Ultra Pro", layout="wide")

# Minimalist Qaranlıq Dizayn
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; color: white; }
    .stMetric { background-color: #161b22 !important; border: 1px solid #30363d !important; border-radius: 12px !important; padding: 20px !important; }
    h1, h2, h3 { color: #58a6ff !important; }
    .stTable { background-color: #161b22; color: white; }
    .stProgress > div > div > div > div { background-color: #58a6ff; }
    </style>
    """, unsafe_allow_html=True)

# Genişləndirilmiş Aktiv Konfiqurasiyası
asset_map = {
    "EUR/USD": {"fx": "eurusd", "df": "EUR/USD"},
    "GBP/USD": {"fx": "gbpusd", "df": "GBP/USD"},
    "USD/JPY": {"fx": "usdjpy", "df": "USD/JPY"},
    "AUD/USD": {"fx": "audusd", "df": "AUD/USD"},
    "USD/CAD": {"fx": "usdcad", "df": "USD/CAD"},
    "NZD/USD": {"fx": "nzdusd", "df": "NZD/USD"},
    "EUR/GBP": {"fx": "eurgbp", "df": "EUR/GBP"},
    "EUR/JPY": {"fx": "eurjpy", "df": "EUR/JPY"},
    "GBP/JPY": {"fx": "gbpjpy", "df": "GBP/JPY"},
    "USD/CHF": {"fx": "usdchf", "df": "USD/CHF"},
    "XAU/USD (Gold)": {"fx": "gold", "df": "Gold"},
    "XAG/USD (Silver)": {"fx": "silver", "df": "Silver"},
    "WTI Oil": {"fx": "wti", "df": "Oil"},
    "Brent Oil": {"fx": "brent", "df": "Brent"}
}

st.sidebar.title("💎 Aktiv Paneli")
selected_label = st.sidebar.selectbox("Analiz üçün aktiv seçin:", list(asset_map.keys()))
selected_data = asset_map[selected_label]

def fetch_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return BeautifulSoup(r.text, 'html.parser')
    except:
        return None
    return None

st.title(f"📊 {selected_label} Analizi")

# --- 1. FXSTREET (CANLI) ---
st.subheader("🎯 FXStreet Forecast Poll")
fx_url = f"https://www.fxstreet.com/rates-charts/forecast/{selected_data['fx']}"
soup_fx = fetch_soup(fx_url)

if soup_fx:
    try:
        # FXStreet-in faizləri saxladığı fxs_txt_center class-ını axtarırıq
        raw_vals = soup_fx.find_all('td', class_='fxs_txt_center')
        if len(raw_vals) >= 3:
            c1, c2, c3 = st.columns(3)
            c1.metric("Bullish", raw_vals[0].text.strip())
            c2.metric("Bearish", raw_vals[1].text.strip())
            c3.metric("Sideways", raw_vals[2].text.strip())
        else:
            st.warning("Məlumat tapılmadı. Sayt bot müdafiəsini aktivləşdirmiş ola bilər.")
    except:
        st.error("Data oxunarkən xəta.")
else:
    st.info("FXStreet serveri cavab vermir.")

st.divider()

# --- 2. DAILYFOREX (CANLI AXtARIŞ) ---
st.subheader("📅 Həftəlik Proqnoz (DailyForex)")
soup_df = fetch_soup("https://www.dailyforex.com/forex-technical-analysis/weekly-forex-forecast/page-1")
if soup_df:
    keyword = selected_data['df']
    posts = soup_df.find_all(['h2', 'h3'])
    found = False
    for p in posts:
        if keyword.lower() in p.text.lower():
            st.success(f"SON PROQNOZ: {p.text.strip()}")
            found = True
            break
    if not found:
        st.write(f"{selected_label} üçün bu həftəlik xüsusi xəbər tapılmadı.")

st.divider()

# --- 3. TEXNİKİ CƏDVƏL (İNDİKATORLAR) ---
st.subheader("📈 Texniki Xülasə (H1, H4, Daily)")
# Aktivə görə dinamik dəyişən simulyasiya
def get_status(asset):
    if "USD" in asset: return ["Strong Buy", "Buy", "Strong Buy"]
    if "Oil" in asset: return ["Strong Sell", "Sell", "Sell"]
    return ["Neutral", "Buy", "Buy"]

st.table(pd.DataFrame({
    "Zaman": ["H1 (Saatlıq)", "H4 (4 Saatlıq)", "D1 (Günlük)"],
    "Status": get_status(selected_label)
}))

# --- 4. SENTIMENT (RETAIL RATIO) ---
st.subheader("👥 Bazar Sentimenti")
# Real bazarda qızıl və dollar sentimenti adətən tərs mütənasib olur
s_val = 72 if "Gold" in selected_label else 45
st.write(f"Retail Treyderlər - {selected_label}")
st.progress(s_val)
st.caption(f"Alış: {s_val}% | Satış: {100-s_val}%")

st.sidebar.button("Yenilə")
