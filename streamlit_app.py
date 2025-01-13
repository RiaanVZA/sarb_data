""" Simple application to fetch SARB Market Rates from SARB API and display.
"""

import streamlit as st
from sarb_api import sarb
import pandas as pd
from datetime import datetime,timedelta

def get_api_data():

    rates_data_df = sarb.fetch_all_rates()
    df = sarb.convert_data_to_dataframe(rates_data_df)
    df = df[["SectionName", "SectionId", "TimeseriesCode", "Name", "Value", "UpDown", "Date"]]
    
    return df


def get_timeseries_data(tscode: str, start_date: str, end_date: str):

    df = sarb.fetch_timeseries_data(tscode, start_date, end_date)
        
    return df

def map_updown(change: int):

    if change == 1:
        return '<span style="color:green;"> ▲ </span>'  # Up arrow
    elif change == 0: 
        return '<span style="color:gray;"> = </span>'  # No change
    elif change == -1: 
        return '<span style="color:red;"> ▼ </span>'  # Down arrow
    else:
        return ''


def prep_line_chart_data(df):
    df = df.sort_values(by=["Period","Timeseries"], ascending=[True, True])
    df["Period"] = pd.to_datetime(df["Period"])
    df['Period'] = df['Period'].dt.strftime('%Y-%m-%d')

    return df

def draw_line_chart(df):
    st.line_chart(df,x="Period", x_label="Date",y='Value', y_label='Value',color="Timeseries")
    
try:

    # page setup
    st.set_page_config(
        page_title="SARB Rates",
        page_icon=":house:",
        layout="wide",
    )

    MIN_YEAR = 2015
    MAX_YEAR = 2025

    tabs = st.tabs(["Home", "My Charts", "Interest Rates", "Inflation Rates", "Capital Market Rates", "Money Market Rates", "Exchange Rates"])

    # fetch data from SARB APIs
    df = get_api_data()

    with tabs[0]: # home page

        st.title("SARB Market & Exhange Rates", help="https://custom.resbank.co.za/SarbWebApi/Help")

        # define various rate dataframes 
        capital_market_rates_df = df[df["SectionName"] == "Capital Market Rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        inflation_rates_df = df[df["SectionName"] == "Inflation rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        interest_rates_df = df[df["SectionName"] == "Interest rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        exchange_rates_df = df[df["SectionName"] == "Exchange rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        money_market_rates_df = df[df["SectionName"] == "Money Market Rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]

    
        # st.caption("Trends", help="Movement: ▲ for up, ▼ for down, = for no change")

        st.markdown(
        """
        <table width="100%" cellspacing="0" cellpadding="0" style="border:none; font-size:12px;">
            <tr style="border:none;">
                <td style="border:none;">
                Movement: ▲ for up, ▼ for down, = for no change
                </td>
                <td align="right" style="border:none;">
                Like what you see? Please consider supporting my by buying me a coffee.  
                    <a href="https://buymeacoffee.com/riaanv" target="_blank" style="text-decoration: none;">
                    <button style="background-color:#FFDD00; border:none; border-radius:5px; color:black; padding:5px 5px; font-size:12px;">
                        ☕ Buy Me a Coffee
                    </button>
                </a>
                </td>
            </tr>
        </table>
        """,
        unsafe_allow_html=True
    )

        # first container, with Interest, Inflation and Capital Market Rates
        with st.container():
            c1, c2, c3 = st.columns([1,1,3])

        # second container with Money Market and Exchange Rates
        with st.container():
            c4, c5, = st.columns([2,3])

        with c1: # Interest Rates
            st.subheader("Interest Rates", divider="green")
            for index, row in interest_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                """, unsafe_allow_html=True)
                
        with c2: # Inflation Rates
            st.subheader("Inflation Rates", divider="blue")
            for index, row in inflation_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                """, unsafe_allow_html=True)

        with c3: # Capital Market Rates
            st.subheader("Capital Market Rates", divider="violet")
            for index, row in capital_market_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                """, unsafe_allow_html=True)
        
        with c4: # Money Market Rates
            st.subheader("Money Market Rates", divider="red")
            for index, row in money_market_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                """, unsafe_allow_html=True)
            
        with c5: # Exchange Rates
            st.subheader("Exchange Rates", divider="orange")
            # st.table(money_market_rates_df) #,hide_index=False)
            for index, row in exchange_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name}: <strong>R {row['Value']}</strong>{map_updown(row['UpDown'])}</li>
                """, unsafe_allow_html=True)
     
        # third container with Data Table
        with st.container(): # Data Table  
        
            st.subheader("", divider="grey")
            st.subheader("Data")

            arrow_mapping = {
                1: "▲",  # Up arrow
                0: "=",  # No change
                -1: "▼"  # Down arrow
            }
            
            column_config = {
                "SectionName": st.column_config.TextColumn(
                    "Category",  # Custom header label
                    help="The name of the category.",  # Tooltip
                ),
                "SectionId": st.column_config.TextColumn(
                    "Code",  # Custom header label
                    help="The rate's code.",  # Tooltip
                ),
                "Name": st.column_config.TextColumn(
                    "Name", # Custom header label
                    help="The name of the rate.", # Toolti
                ),
                "Value": st.column_config.NumberColumn(
                    "Value",
                    # format="%.3f",  # Display numbers with two decimal places
                    help="The value of the rate.",
                ),
                "Date": st.column_config.DateColumn(
                    "Date",
                    format="YYYY-MM-DD",  # Custom date format
                    help="The date associated with the rate. YYYY-MM-DD",
                ),
                "UpDown": st.column_config.TextColumn(
                    "Trend",
                    help="The trend of the rate (▲ for up, ▼ for down, = for no change).",
                ),
                "TimeseriesCode": st.column_config.TextColumn(
                    "TS Code",
                    help="Timeseries Code used by SARB",
                ),
            }

            df["UpDown"] = df["UpDown"].map(arrow_mapping)
            st.dataframe(df, use_container_width=True, hide_index=True, column_config=column_config)

    with tabs[1]: # My charts

        # setup chart selector data.
        unique_options = df["Name"].unique().tolist()
        selected_name = st.selectbox("Select Data Element", options=unique_options, index=9)
        selected_category = df.loc[df["Name"] == selected_name, "SectionName"].squeeze()
        selected_tscode = df.loc[df["Name"] == selected_name, "TimeseriesCode"].squeeze()

        # setup date slider
        st.write("Which years are you interested in?")
        start_year, end_year = st.slider("Chart Date Range", MIN_YEAR, MAX_YEAR, (MIN_YEAR, MAX_YEAR))
        
        start_date = datetime(start_year,1,1).strftime("%Y-%m-%d")
        end_date = datetime(end_year,12,31).strftime("%Y-%m-%d")

        # get timeseries data from SARB using timeseries code.
        ts_df = get_timeseries_data(selected_tscode, start_date, end_date)

        # fine tune dataframe.
        if not ts_df.empty:
            ts_df["Period"] = pd.to_datetime(ts_df["Period"])
            ts_df['Period'] = ts_df['Period'].dt.strftime('%Y-%m-%d')
            selected_description = ts_df.loc[ts_df["Timeseries"] == selected_name, "Description"].unique().squeeze()

            # draw chart and data table.
            st.header(f"{selected_category} - {selected_name}")
            st.caption(selected_description)
            st.line_chart(ts_df,x="Period", x_label="Date",y='Value', y_label="Value",color="Timeseries")
            st.dataframe(ts_df,use_container_width=True)

        else:
            st.write("No Data")

    with tabs[2]: # Interest Rates

        # setup date slider
        st.write("Which years are you interested in?")
        start_year, end_year = st.slider("Interest Rate Date Range", MIN_YEAR, MAX_YEAR, (MIN_YEAR, MAX_YEAR),)
        start_date = datetime(start_year,1,1).strftime("%Y-%m-%d")
        end_date = datetime(end_year,12,31).strftime("%Y-%m-%d")

        # fetch the data 
        ts_df = pd.DataFrame()
        st.header("Interest Rates")

        for index, row in interest_rates_df.iterrows():
            tscode :str = row["TimeseriesCode"]
            df = get_timeseries_data(tscode, start_date, end_date)
            ts_df = pd.concat([ts_df, df], ignore_index=True)
            
        # draw the line chart and data table
        if not ts_df.empty:
           ts_df = prep_line_chart_data(ts_df)
           draw_line_chart(ts_df)
           st.dataframe(ts_df,use_container_width=True, hide_index=True,)

        else:
            st.write("No Data")

    with tabs[3]: # Inflation Rates

        # setup date slider
        st.write("Which years are you interested in?")
        start_year, end_year = st.slider("Inflation Date Range", MIN_YEAR, MAX_YEAR, (MIN_YEAR, MAX_YEAR),)
        start_date = datetime(start_year,1,1).strftime("%Y-%m-%d")
        end_date = datetime(end_year,12,31).strftime("%Y-%m-%d")

        # fetch the data 
        ts_df = pd.DataFrame()
        st.header("Inflation Rates")

        for index, row in inflation_rates_df.iterrows():
            tscode :str = row["TimeseriesCode"]
            df = get_timeseries_data(tscode, start_date, end_date)
            ts_df = pd.concat([ts_df, df], ignore_index=True)
            
        # draw the line chart and data table
        if not ts_df.empty:
           ts_df = prep_line_chart_data(ts_df)
           draw_line_chart(ts_df)
           st.dataframe(ts_df,use_container_width=True, hide_index=True,)

        else:
            st.write("No Data")

    with tabs[4]: # Capital Market Rates

        # setup date slider
        st.header("Capital Market Rates")
        st.write("Which years are you interested in?")
        start_year, end_year = st.slider("Capital Market Rates Date Range", MIN_YEAR, MAX_YEAR, (MIN_YEAR, MAX_YEAR),)
        start_date = datetime(start_year,1,1).strftime("%Y-%m-%d")
        end_date = datetime(end_year,12,31).strftime("%Y-%m-%d")

        # setup multiselector
        options = capital_market_rates_df["Name"].unique()
        selected_options = st.multiselect(
            'Which Capital Market rate(s) would you like to view?'
            , options
             , ["10 years and longer (daily average bond yields)", "5-10 years (daily average bond yields)"]
            )

        # fetch the data 
        ts_df = pd.DataFrame()
        filtered_df = capital_market_rates_df[capital_market_rates_df["Name"].isin(selected_options)]

        for index, row in filtered_df.iterrows():
            tscode :str = row["TimeseriesCode"]
            df = get_timeseries_data(tscode, start_date, end_date)
            ts_df = pd.concat([ts_df, df], ignore_index=True)
            
        # draw the line chart and data table
        if not ts_df.empty:
            ts_df = prep_line_chart_data(ts_df)
            draw_line_chart(ts_df)
            st.dataframe(ts_df,use_container_width=True, hide_index=True,)

        else:
            st.write("No Data")

    with tabs[5]: # Money Market Rates

        # setup date slider
        st.header("Money Market Rates")
        st.write("Which years are you interested in?")
        start_year, end_year = st.slider("Money Market Rates Date Range", MIN_YEAR, MAX_YEAR, (MIN_YEAR, MAX_YEAR),)
        start_date = datetime(start_year,1,1).strftime("%Y-%m-%d")
        end_date = datetime(end_year,12,31).strftime("%Y-%m-%d")

         # setup multiselector
        options = money_market_rates_df["Name"].unique()
        selected_options = st.multiselect(
            'Which Money Market rate would you like to view?'
            , options
            , ['Treasury bills - 91 day (tender rates)', 'Treasury bills - 182 day (tender rates)', 'Treasury bills - 273 day (tender rates)','Treasury bills - 364 day (tender rates)'])

        # fetch the data 
        ts_df = pd.DataFrame()
        filtered_df = money_market_rates_df[money_market_rates_df["Name"].isin(selected_options)]
        
        for index, row in filtered_df.iterrows():
            tscode :str = row["TimeseriesCode"]
            df = get_timeseries_data(tscode, start_date, end_date)
            ts_df = pd.concat([ts_df, df], ignore_index=True)
            
        # draw the line chart and data table
        if not ts_df.empty:
           ts_df = prep_line_chart_data(ts_df)
           draw_line_chart(ts_df)
           st.dataframe(ts_df,use_container_width=True, hide_index=True,)

        else:
            st.write("No Data")

    with tabs[6]: # Exchange Rates

        # setup date slider
        st.header("Exchange Rates",divider="orange")
        st.write("Which years are you interested in?")
        start_year, end_year = st.slider("Exchange Rate Date Range", MIN_YEAR, MAX_YEAR, (MIN_YEAR, MAX_YEAR),)
        start_date = datetime(start_year,1,1).strftime("%Y-%m-%d")
        end_date = datetime(end_year,12,31).strftime("%Y-%m-%d")

        # setup multiselector
        options = exchange_rates_df["Name"].unique()
        selected_options = st.multiselect(
            'Which exchange rates would you like to view?'
            , options
            , ['Rand per US Dollar', 'Rand per British Pound', 'Rand per Euro'])

        # fetch the data 
        ts_df = pd.DataFrame()
        filtered_df = exchange_rates_df[exchange_rates_df["Name"].isin(selected_options)]

        for index, row in filtered_df.iterrows():
            tscode :str = row["TimeseriesCode"]
            df = get_timeseries_data(tscode, start_date, end_date)
            ts_df = pd.concat([ts_df, df], ignore_index=True)
            
        # draw the line chart and data table
        if not ts_df.empty:
            ts_df = prep_line_chart_data(ts_df)
            draw_line_chart(ts_df)
            st.dataframe(ts_df,use_container_width=True, hide_index=True,)

        else:
            st.write("No Data")

    
        

except Exception as err:
    raise err 


