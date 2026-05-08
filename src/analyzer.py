import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_crypto(symbol: str, price: float, change: float):
    """AI ile kripto analizi yapar"""
    
    prompt = f"""
    {symbol.upper()} kripto parası için kısa bir analiz yap:
    - Güncel fiyat: ${price}
    - 24 saatlik değişim: %{change}
    
    Kısa ve anlaşılır şekilde Türkçe olarak:
    1. Piyasa durumu nasıl?
    2. Bu değişim ne anlama geliyor?
    3. Yatırımcılar ne yapmalı?
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    
    return response.choices[0].message.content