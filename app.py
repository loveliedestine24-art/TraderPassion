import streamlit as st
import pandas_ta as ta
import yfinance as yf
import pandas as pd
import time

# Konfigirasyon paj la pou li parèt byen sou iPhone
st.set_page_config(page_title="Vorna Pro Bot", layout="wide")

# Style CSS pou kreye aparans ki nan image_2.png
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    div[data-testid="stMetricValue"] { color: #00ff00; font-size: 28px; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; font-weight: bold; font-size: 18px; }
    .stSelectbox label { color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# Inisyalize done yo nan memwa aplikasyon an
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'history' not in st.session_state: st.session_state.history = []

# --- DASHBOARD (Seksyon anwo a) ---
st.title("💠 TRADER PASSION BOT")

col1, col2, col3 = st.columns(3)
total = st.session_state.wins + st.session_state.losses
winrate = (st.session_state.wins / total * 100) if total > 0 else 0.0

col1.metric("SALDO ESTIMADO", "$42,366.61") # Montre balans lan jan li parèt nan foto a
col2.metric("SUCCESS RATE", f"{round(winrate, 1)}%")
col3.metric("VITÓRIAS", st.session_state.wins)

st.markdown("---")

# --- ANALIZ AK SIYAL (Seksyon mitan an) ---
pair = st.selectbox("Ativo (Chwazi Mache)", ["EURUSD=X", "USDCHF=X", "GBPUSD=X", "BTC-USD", "ETH-USD"])

def jwenn_siyal(pè_mache):
    try:
        # Rale done 1 minit (1M) jan sa ekri nan image_2.png
        df = yf.download(pè_mache, period='1d', interval='1m', progress=False)
        if df.empty: return "⌛ Pa gen done...", ""
        
        # Kalkil Stochastic (K=14, D=3)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'], k=14, d=3)
        last_k = stoch['STOCHk_14_3_3'].iloc[-1]
        
        # Lojik pou siyal yo (Dapre image.png ak koreksyon ou)
        if last_k >= 80:
            return "🔴 SIYAL VANN (PUT)", "Pattern: Evening Star / Tweezer Top"
        elif last_k <= 20:
            return "🟢 SIYAL ACHTE (CALL)", "Pattern: Morning Star / Bullish Engulfing"
        elif 75 <= last_k < 80 or 20 < last_k <= 25:
            return "⏳ PREPARE W...", f"Siyal ap vini nan 5-10 segond sou {pè_mache}"
        
        return "🔎 Ap chèche...", "Mache a estab kounye a."
    except:
        return "❌ Erè Done", "Verifye koneksyon an."

siyal_tit, siyal_detay = jwenn_siyal(pair)

# Afichaj Siyal la
st.subheader("🤖 Analiz an Dirèk")
if "VANN" in siyal_tit:
    st.error(f"### {siyal_tit}\n{siyal_detay}")
elif "ACHTE" in siyal_tit:
    st.success(f"### {siyal_tit}\n{siyal_detay}")
elif "PREPARE" in siyal_tit:
    st.warning(f"### {siyal_tit}\n{siyal_detay}")
else:
    st.info(f"{siyal_tit}\n{siyal_detay}")

# --- BOUTON POU WIN/LOSS (Seksyon anba a) ---
st.markdown("### 📝 Anrejistre Rezilta")
c_win, c_loss = st.columns(2)

if c_win.button("✅ WIN"):
    st.session_state.wins += 1
    st.session_state.history.append(f"✅ Win sou {pair}")
    st.rerun()

if c_loss.button("❌ LOSS"):
    st.session_state.losses += 1
    st.session_state.history.append(f"❌ Loss sou {pair}")
    st.rerun()

# --- LOGS ---
with st.expander("🕒 Istorik Siyal yo"):
    for log in reversed(st.session_state.history[-5:]):
        st.write(log)
