import requests 
import pandas as pd
from tabulate import tabulate

def display_data(df):
    """ Display the contets of a dataframe.
    """
       
    try:

        # create a sub section (view)
        df_view = df[["SectionName", "Name", "Value", "Date"]]

        #print the contents of the dataframe in a table
        colalign = ["left", "left", "left", "right", "center"]
        print(tabulate(df_view, headers='keys', tablefmt='presto', colalign=colalign))

    except Exception as err:
        raise err 

def fetch_data(api_url: str) -> str:
    """ fetch data from SARB API
    """

    try:

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()  
            return data           
        else:
            print("{'Status_Code': '%s!'}" % response.status_code)

    except Exception as err:
        print("Something went wrong!")   

def convert_data_to_dataframe(data) -> pd.DataFrame:
    """ convert JSON data received from API to dataframe
    """

    try:

        df = pd.DataFrame(data)
        df["Value"] = pd.to_numeric(df["Value"])
        df["Date"] = pd.to_datetime(df["Date"])

        return df


    except Exception as err:
        print("Something went wrong!")   


def fetch_home_page_rates():
    # fetch home page rates
    print("Fetching latest Home Page Rates from SARB.")
    data = fetch_data("https://custom.resbank.co.za/SarbWebApi/WebIndicators/HomePageRates")
    display_data(convert_data_to_dataframe(data))

def fetch_market_rates():
    # fetch home page rates
    print("Fetching latest Current Market Rates from SARB.")
    data = fetch_data("https://custom.resbank.co.za/SarbWebApi/WebIndicators/CurrentMarketRates")
    display_data(convert_data_to_dataframe(data))

def fetch_historical_exchange_rates():
    # fetch home page rates
    print("Fetching latest Historical Exchange Rates (Daily) from SARB.")
    data = fetch_data("https://custom.resbank.co.za/SarbWebApi/WebIndicators/HistoricalExchangeRatesDaily")
    display_data(convert_data_to_dataframe(data))
