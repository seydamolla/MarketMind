from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

def show_result(data: dict, analysis: str):
    """Sonuçları güzel bir şekilde gösterir"""
    
    # Fiyat tablosu
    table = Table(box=box.ROUNDED, style="cyan")
    table.add_column("Özellik", style="bold white")
    table.add_column("Değer", style="bold green")
    
    table.add_row("💰 Sembol", data["symbol"].upper())
    table.add_row("💵 Fiyat", f"${data['price']:,.2f}")
    
    change = data["change_24h"]
    change_color = "green" if change >= 0 else "red"
    change_icon = "📈" if change >= 0 else "📉"
    table.add_row(
        "24s Değişim",
        f"[{change_color}]{change_icon} %{change}[/{change_color}]"
    )
    
    console.print(table)
    
    # AI analizi
    console.print(Panel(
        analysis,
        title="🤖 AI Analizi",
        style="yellow"
    ))