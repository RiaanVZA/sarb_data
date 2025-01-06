### Simple application to fetch SARB Market Rates from SARB API and display.
###

import requests 
import pandas as pd
from tabulate import tabulate

# Print DataFrame using tabulate




#globals



def fetch_market_rates():
    """ fetch market rates

    """

    api_url = "https://custom.resbank.co.za/SarbWebApi/WebIndicators/CurrentMarketRates"

    try:

        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()  
            df = pd.DataFrame(data)
            df["Value"] = pd.to_numeric(df["Value"])
            df["Date"] = pd.to_datetime(df["Date"])

            # print(df.dtypes)
            df_view = df[["SectionName", "Name", "Value", "Date"]]

            #print the contents of the dataframe in a table
            # first, we prep the table
            colalign = ["left", "left", "left", "right", "center"]
            print(tabulate(df_view, headers='keys', tablefmt='presto', colalign=colalign))
    

            # for row in data:
            #     print(type(row))
            #     rates = row.get("Name", "N/A")
            #     values = row.get("Value", "N/A")
            #     dates = row.get("Date", "N/A")
            #     print(rates, values, "-", dates)
            
        else:
            print("{'Status_Code': '%s!'}" % response.status_code)

    except Exception as err:
        print("Something went wrong!")   


def main():
    """ Main Workflow Function
    """

    try:
        # fetch market rates
        print("Fetching latest Market Rates from SARB.")
        # print("." * 200)
        fetch_market_rates()


    except Exception as error:
        raise error

    finally:
    # Close the connection
        # print("." * 200)
        print("Done.")

if __name__ == "__main__":
    main()

