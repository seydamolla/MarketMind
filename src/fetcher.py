import requests

def get_crypto_price(symbol: str):
    """CoinGecko'dan kripto fiyatı çeker"""
    
    url = "https://api.coingecko.com/api/v3/simple/price"
    
    params = {
        "ids": symbol,
        "vs_currencies": "usd",
        "include_24hr_change": "true"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if symbol in data:
            price = data[symbol]["usd"]
            change = data[symbol]["usd_24h_change"]
            return {"symbol": symbol, "price": price, "change_24h": round(change, 2)}
        else:
            return None
            
    except Exception as e:
        print(f"Hata: {e}")
        return None

def get_crypto_history(symbol: str):
    """7 günlük fiyat geçmişi çeker"""
    
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    
    params = {
        "vs_currency": "usd",
        "days": "7"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        prices = data["prices"]
        return prices
        
    except Exception as e:
        print(f"Hata: {e}")
        return []