import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from src.fetcher import get_crypto_price, get_crypto_history
from src.analyzer import analyze_crypto

st.set_page_config(
    page_title="MarketMind",
    page_icon="📈",
    layout="wide"
)

st.title("📈 MarketMind — AI Destekli Kripto Analiz")
st.markdown("---")

# Kullanıcı girişi
symbol = st.text_input(
    "Kripto sembolü gir:",
    placeholder="örn: bitcoin, ethereum, solana"
).strip().lower()

if st.button("🔍 Analiz Et") and symbol:
    
    with st.spinner("Veri çekiliyor..."):
        data = get_crypto_price(symbol)
    
    if not data:
        st.error("❌ Sembol bulunamadı! Tekrar dene.")
    else:
        # Üst metrikler
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("💰 Fiyat", f"${data['price']:,.2f}")
        with col2:
            st.metric("📊 24s Değişim", f"%{data['change_24h']}")
        with col3:
            st.metric("🪙 Sembol", data["symbol"].upper())
        
        st.markdown("---")
        
        # Grafik
        with st.spinner("Grafik hazırlanıyor..."):
            history = get_crypto_history(symbol)
        
        if history:
            dates = [datetime.fromtimestamp(p[0]/1000) for p in history]
            prices = [p[1] for p in history]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=dates,
                y=prices,
                mode="lines",
                name=symbol.upper(),
                line=dict(color="#00ff88", width=2)
            ))
            fig.update_layout(
                title=f"{symbol.upper()} — 7 Günlük Fiyat Grafiği",
                xaxis_title="Tarih",
                yaxis_title="Fiyat (USD)",
                template="plotly_dark",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # AI Analizi
        with st.spinner("🤖 AI analiz yapıyor..."):
            analysis = analyze_crypto(
                data["symbol"],
                data["price"],
                data["change_24h"]
            )
        
        st.markdown("### 🤖 AI Analizi")
        st.info(analysis)