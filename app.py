import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from src.fetcher import get_crypto_price, get_crypto_history, get_stock_price, get_stock_history
from src.analyzer import analyze_crypto

st.set_page_config(
    page_title="MarketMind",
    page_icon="📈",
    layout="wide"
)

st.title("📈 MarketMind — AI Destekli Kripto & Hisse Analiz")
st.markdown("---")

# Sekmeler
tab1, tab2 = st.tabs(["🪙 Kripto", "📊 BIST Hisse"])

# --- KRİPTO SEKMESİ ---
with tab1:
    symbol = st.text_input(
        "Kripto sembolü gir:",
        placeholder="örn: bitcoin, ethereum, solana",
        key="crypto"
    ).strip().lower()

    if st.button("🔍 Analiz Et", key="crypto_btn") and symbol:
        
        with st.spinner("Veri çekiliyor..."):
            data = get_crypto_price(symbol)
        
        if not data:
            st.error("❌ Sembol bulunamadı! Tekrar dene.")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Fiyat", f"${data['price']:,.2f}")
            with col2:
                change = data['change_24h']
                st.metric("📊 24s Değişim", f"%{change}", delta=f"{change}%")
            with col3:
                st.metric("🪙 Sembol", data["symbol"].upper())
            
            st.markdown("---")
            
            with st.spinner("Grafik hazırlanıyor..."):
                history = get_crypto_history(symbol)
            
            if history:
                dates = [datetime.fromtimestamp(p[0]/1000) for p in history]
                prices = [p[1] for p in history]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates, y=prices,
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
            
            with st.spinner("🤖 AI analiz yapıyor..."):
                analysis = analyze_crypto(data["symbol"], data["price"], data["change_24h"])
            
            st.markdown("### 🤖 AI Analizi")
            st.info(analysis)

# --- HİSSE SEKMESİ ---
with tab2:
    st.markdown("**Örnek semboller:** POLTK.IS, THYAO.IS, GARAN.IS, ASELS.IS")
    
    ticker = st.text_input(
        "Hisse sembolü gir:",
        placeholder="örn: THYAO.IS, POLTK.IS",
        key="stock"
    ).strip().upper()

    if st.button("🔍 Analiz Et", key="stock_btn") and ticker:
        
        with st.spinner("Veri çekiliyor..."):
            data = get_stock_price(ticker)
        
        if not data:
            st.error("❌ Hisse bulunamadı! Sembolün sonuna .IS ekle (örn: THYAO.IS)")
        else:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Fiyat", f"₺{data['price']:,.2f}")
            with col2:
                change = data['change_24h']
                st.metric("📊 Değişim", f"%{change}", delta=f"{change}%")
            with col3:
                st.metric("🏢 Şirket", data["name"][:20])
            
            st.markdown("---")
            
            with st.spinner("Grafik hazırlanıyor..."):
                history = get_stock_history(ticker)
            
            if history:
                dates = [p[0] for p in history]
                prices = [p[1] for p in history]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dates, y=prices,
                    mode="lines",
                    name=ticker,
                    line=dict(color="#ff9900", width=2)
                ))
                fig.update_layout(
                    title=f"{ticker} — 7 Günlük Fiyat Grafiği",
                    xaxis_title="Tarih",
                    yaxis_title="Fiyat (₺)",
                    template="plotly_dark",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with st.spinner("🤖 AI analiz yapıyor..."):
                analysis = analyze_crypto(data["symbol"], data["price"], data["change_24h"])
            
            st.markdown("### 🤖 AI Analizi")
            st.info(analysis)