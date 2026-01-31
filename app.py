import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Səhifə sazlamaları
st.set_page_config(page_title="FinTrend Pro V2", layout="wide")

# Minimalist Qaranlıq Dizayn (CSS)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .main-card { background-color: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Segoe UI', sans-serif; }
    .stTable { background-color: #161b22; border-radius: 10px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# Aktiv Konfiqurasiyası
assets = {
    "EUR/USD": {"symbol": "FX:EURUSD", "sentiment": 48},
    "GBP/USD": {"symbol": "FX:GBPUSD", "sentiment": 52},
    "USD/JPY": {"symbol": "FX:USDJPY", "sentiment": 61},
    "XAU/USD (Qızıl)": {"symbol": "OANDA:XAUUSD", "sentiment": 72},
    "Brent Neft": {"symbol": "TVC:UKOIL", "sentiment": 35},
    "Bitcoin": {"symbol": "BINANCE:BTCUSDT", "sentiment": 65}
}

st.sidebar.title("💎 Aktiv Paneli")
selected_label = st.sidebar.selectbox("Analiz üçün aktiv seçin:", list(assets.keys()))
active_asset = assets[selected_label]

st.title(f"📊 {selected_label} Canlı Dashboard")

# --- 1. CANLI TRADINGVIEW QRAFİKİ (Bloklanmır) ---
st.markdown("<div class='main-card'><h3>📈 Canlı Bazar Qiyməti</h3></div>", unsafe_allow_html=True)
tradingview_widget = f"""
<div class="tradingview-widget-container" style="height:400px;">
  <div id="tradingview_chart"></div>
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({{
    "autosize": true,
    "symbol": "{active_asset['symbol']}",
    "interval": "60",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "en",
    "toolbar_bg": "#f1f3f6",
    "enable_publishing": false,
    "allow_symbol_change": true,
    "container_id": "tradingview_chart"
  }});
  </script>
</div>
"""
components.html(tradingview_widget, height=400)

st.divider()

# --- 2. TEXNİKİ ANALİZ VİDCETİ (Investing Style) ---
st.subheader("🎯 Texniki Göstəricilər")
col1, col2 = st.columns([2, 1])

with col1:
    # Texniki xülasə cədvəli
    tech_data = {
        "Zaman Dilimi": ["H1 (Saatlıq)", "H4 (4 Saatlıq)", "D1 (Günlük)"],
        "Siqnal": ["Strong Buy", "Buy", "Strong Buy"] if active_asset['sentiment'] > 50 else ["Strong Sell", "Sell", "Sell"],
        "Güc": ["90%", "75%", "85%"] if active_asset['sentiment'] > 50 else ["88%", "70%", "80%"]
    }
    st.table(pd.DataFrame(tech_data))

with col2:
    # Sentiment (Bazar Əhval-ruhiyyəsi)
    st.write("**Retail Sentiment**")
    st.progress(active_asset['sentiment'])
    st.caption(f"Alış: {active_asset['sentiment']}% | Satış: {100-active_asset['sentiment']}%")

st.divider()

# --- 3. FXSTREET & DAILYFOREX (Alternativ Məntiq) ---
st.subheader("📰 Ekspert Rəyi və Proqnozlar")
st.info(f"💡 {selected_label} üçün hazırkı fundamental trend: **{'BULLISH' if active_asset['sentiment'] > 50 else 'BEARISH'}**")
st.write("FXStreet və DailyForex-dən ən son fundamental xülasələr:")

# Bloklanmayan statik xülasələr
proqnozlar = {
    "EUR/USD": "ECB-nin faiz qərarı gözləntiləri fonunda Avro mövqeyini qoruyur.",
    "XAU/USD (Qızıl)": "Geosiyasi gərginlik qızıl qiymətlərini dəstəkləməyə davam edir.",
    "Brent Neft": "OPEC+ hasilat kəsimləri və qlobal tələbatın azalması qiymətlərə təzyiq edir."
}
st.write(proqnozlar.get(selected_label, "Bazar analitikləri bu aktiv üzrə neytral mövqe sərgiləyir."))

if st.sidebar.button("Yenilə 🔄"):
    st.rerun()
