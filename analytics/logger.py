import duckdb
from datetime import datetime
import os
from rich.console import Console
from rich.table import Table

console = Console()
DB_PATH = "chaos_metrics.db"

def init_db():
    conn = duckdb.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS strikes (
            timestamp TIMESTAMP,
            target_layer VARCHAR,
            severity VARCHAR
        )
    """)
    conn.close()

def log_strike(target_layer, severity):
    if not os.path.exists(DB_PATH):
        init_db()
    conn = duckdb.connect(DB_PATH)
    conn.execute("INSERT INTO strikes VALUES (?, ?, ?)", (datetime.now(), target_layer, severity))
    conn.close()
    
def show_report():
    if not os.path.exists(DB_PATH):
        init_db()
    conn = duckdb.connect(DB_PATH)
    
    # Use fetchall() instead of fetchdf() to drop the massive pandas/numpy requirement
    results = conn.execute("SELECT target_layer, severity, COUNT(*) FROM strikes GROUP BY target_layer, severity").fetchall()
    
    console.print("\n[bold cyan]📊 Chaos Resilience Analytics (DuckDB)[/bold cyan]")
    
    if not results:
        console.print("[italic]No strikes recorded yet.[/italic]")
    else:
        table = Table(show_header=True, header_style="bold magenta", border_style="cyan")
        table.add_column("Target Layer", width=15)
        table.add_column("Severity", width=15)
        table.add_column("Hits", justify="right", width=10)
        
        for row in results:
            table.add_row(row[0].upper(), row[1].upper(), str(row[2]))
            
        console.print(table)
        
    conn.close()
