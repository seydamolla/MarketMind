from src.fetcher import get_crypto_price
from src.analyzer import analyze_crypto
from src.display import show_result
from rich.console import Console

console = Console()

def main():
    console.print("\n[bold cyan]🚀 MarketMind — AI Destekli Kripto Analiz[/bold cyan]\n")
    
    # Kullanıcıdan sembol al
    symbol = input("Kripto sembolü gir (örn: bitcoin, ethereum, solana): ").strip().lower()
    
    console.print(f"\n[yellow]⏳ {symbol.upper()} verisi çekiliyor...[/yellow]")
    
    # Veri çek
    data = get_crypto_price(symbol)
    
    if not data:
        console.print("[red]❌ Sembol bulunamadı! Tekrar dene.[/red]")
        return
    
    console.print("[yellow]🤖 AI analiz yapıyor...[/yellow]\n")
    
    # AI analizi
    analysis = analyze_crypto(data["symbol"], data["price"], data["change_24h"])
    
    # Göster
    show_result(data, analysis)

if __name__ == "__main__":
    main()