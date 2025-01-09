import requests 
import pandas as pd

def GET_data(api_url: str) -> str:
    """ 
    Fetch data from any given SARB API.
    """

    try:

        response = requests.get(api_url)

        if response.status_code == 200:
            parsed_json = response.json() 
            return parsed_json           
        else:
            print("{'Status_Code': '%s!'}" % response.status_code)

    except Exception as err:
        print("Something went wrong!")

def GET_timeseries_data(tscode: str) -> str:
    """ 
    Fetch graph data from SARS based on a specific timeseries code.
    """

    try:

        request_str = f"https://custom.resbank.co.za/SarbWebApi/WebIndicators/Shared/GetTimeseriesObservations/{tscode}"
        response = requests.get(request_str)

        if response.status_code == 200:
            parsed_json = response.json() 
            return parsed_json           
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

        df_sorted = df.sort_values(by=["SectionName", "SectionId", "Name", "Date"], ascending=[True, True, True, True])
        df_distinct = df_sorted.drop_duplicates(subset=["Name"])

        return df_distinct


    except Exception as err:
        print("Something went wrong!")   

def fetch_all_rates() -> str:
    """
    Fetch all the rates from SARB API
    """

    try:

        rates_df = pd.DataFrame()

        rates_apis ={
            "HomePageRates":"https://custom.resbank.co.za/SarbWebApi/WebIndicators/HomePageRates"
            , "CurrentMarketRates": "https://custom.resbank.co.za/SarbWebApi/WebIndicators/CurrentMarketRates"
            # , "DailyExcahngeRates": "https://custom.resbank.co.za/SarbWebApi/WebIndicators/HistoricalExchangeRatesDaily"
            }

        for rate, api_url in rates_apis.items():
          
            # 1. fetch the data from the API -> JSON String (parsed)
            api_data_str = GET_data(api_url)

            # 2. convert the string into a pandas dataframe 
            api_data_df = pd.DataFrame(api_data_str)

            # 3. Append the API data to the existing rates dataframe. 
            rates_df = pd.concat([rates_df, api_data_df], ignore_index=True)

        return rates_df

    except Exception as err:
        raise err
 

def fetch_timeseries_data(tscode: str) -> str:
    """
    Fetch timeseries data from SARB API based on tscode
    """

    try:

        ts_df = pd.DataFrame()    
          
        # 1. fetch the data from the API -> JSON String (parsed)
        api_timeseries_data_str = GET_timeseries_data(tscode)
       
        # 2. convert the string into a pandas dataframe 
        ts_df = pd.DataFrame(api_timeseries_data_str)
        
        return ts_df

    except Exception as err:
        raise err
 