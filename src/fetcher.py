import requests
import yfinance as yf

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

def get_stock_price(ticker: str):
    """Yahoo Finance'dan BIST hisse fiyatı çeker"""
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        price = info.get("currentPrice") or info.get("regularMarketPrice")
        change = info.get("regularMarketChangePercent", 0)
        name = info.get("longName", ticker)
        
        if price:
            return {
                "symbol": ticker,
                "name": name,
                "price": price,
                "change_24h": round(change, 2)
            }
        else:
            return None
            
    except Exception as e:
        print(f"Hata: {e}")
        return None

def get_stock_history(ticker: str):
    """7 günlük hisse geçmişi çeker"""
    
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="7d")
        
        prices = []
        for date, row in hist.iterrows():
            prices.append([date, row["Close"]])
        
        return prices
        
    except Exception as e:
        print(f"Hata: {e}")
        return []