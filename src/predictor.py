import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def predict_tomorrow(symbol: str, prices: list, current_price: float, change: float):
    """Geçmiş verilerden yarın tahmini yapar"""
    
    if not prices:
        return None
    
    # Son 7 günün fiyatları
    price_values = [p[1] for p in prices[-7:]]
    
    # Trend hesapla
    if len(price_values) >= 2:
        trend = ((price_values[-1] - price_values[0]) / price_values[0]) * 100
    else:
        trend = 0
    
    prompt = f"""
    {symbol.upper()} için yarın tahmini yap:
    - Güncel fiyat: ${current_price}
    - 24 saatlik değişim: %{change}
    - 7 günlük trend: %{round(trend, 2)}
    - Son 7 gün fiyatları: {[round(p, 2) for p in price_values]}
    
    Sadece şu formatta Türkçe cevap ver:
    TAHMİN: [YÜKSELİŞ/DÜŞÜŞ/YATAY]
    ORAN: %[sayı]
    SEBEP: [1 cümle açıklama]
    GÜVEN: [DÜŞÜK/ORTA/YÜKSEK]
    
    Not: Bu bir tahmin, yatırım tavsiyesi değildir.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )
    
    return response.choices[0].message.content