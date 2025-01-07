### Simple application to fetch SARB Market Rates from SARB API and display.
###


import typer
from sarb_api import sarb

app = typer.Typer()

@app.command()
def home_page_rates():
    sarb.fetch_home_page_rates()
   
@app.command()
def market_rates():
    sarb.fetch_market_rates()

@app.command()
def historical_exchange_rates_daily():
    sarb.fetch_historical_exchange_rates()

def main():
    app()
    
if __name__ == "__main__":
     main()

