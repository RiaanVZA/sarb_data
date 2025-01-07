### Simple application to fetch SARB Market Rates from SARB API and display.
###


import typer
from sarb_api import sarb

app = typer.Typer()

@app.command()
def home_page_rates(save_to_csv: bool = False, email: bool = False):
    """
    Fetch and view the Home Page Rates from SARB API.

    Parameters:
    - save_to_csv: Expects a boolean, True to save to CSV. Default is False  (optional)
    - email: E-mail a copy of the CSV file.
    """
    sarb.fetch_home_page_rates(save_to_csv, email)

@app.command()
def market_rates(save_to_csv: bool = False):
    """
    Fetch and view the Current Market Rates from SARB API.
    
    Parameters:
    - save_to_csv: Expects a boolean, True to save to CSV. Default is False  (optional)
    """
    sarb.fetch_market_rates(save_to_csv)

@app.command()
def daily_exchange_rates(save_to_csv: bool = False):
    """
    Fetch and view the Daily Exchange Rates from SARB API.
    
    Parameters:
    - save_to_csv: Expects a boolean, True to save to CSV. Default is False  (optional)
    """
    sarb.fetch_historical_exchange_rates(save_to_csv)

def main():
    app()
    
if __name__ == "__main__":
     main()

