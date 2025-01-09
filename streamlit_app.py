""" Simple application to fetch SARB Market Rates from SARB API and display.
"""


import streamlit as st
from sarb_api import sarb
import streamlit_option_menu
from streamlit_option_menu import option_menu
import pandas as pd

def get_api_data():

    rates_data_df = sarb.fetch_all_rates()
    df = sarb.convert_data_to_dataframe(rates_data_df)
    df = df[["SectionName", "SectionId", "TimeseriesCode", "Name", "Value", "UpDown", "Date"]]
    
    return df

def get_timeseries_data(tscode: str):

    df = sarb.fetch_timeseries_data(tscode)
        
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

 
try:

    # page setup
    st.set_page_config(
        page_title="SARB Rates",
        page_icon=":house:",
        layout="wide",
    )

    # st.title("SARB Market & Exhange Rates", help="https://custom.resbank.co.za/SarbWebApi/Help")

    # fetch data from SARB APIs
    df = get_api_data()

    # setup sidebar
    with st.sidebar:
        selected = option_menu(
        menu_title = "Options",
        options = ["Home","Charts"],
        icons = ["house","bar-chart-fill"],
        menu_icon = "cast",
        default_index = 0,
        #orientation = "horizontal",
    )


    if selected == "Charts":

        # st.title('Select Data Element')
        unique_options = df["Name"].unique().tolist()
        selected_name = st.selectbox("Select Data Element", options=unique_options, index=5)

        selected_category = df.loc[df["Name"] == selected_name, "SectionName"].squeeze()
        selected_tscode = df.loc[df["Name"] == selected_name, "TimeseriesCode"].squeeze()

        ts_df = get_timeseries_data(selected_tscode)
        ts_df["Period"] = pd.to_datetime(ts_df["Period"])
        ts_df['Period'] = ts_df['Period'].dt.strftime('%Y-%m-%d')

        selected_description = ts_df.loc[ts_df["Timeseries"] == selected_name, "Description"].unique().squeeze()

        
        st.header(f"{selected_category} - {selected_name}")
        st.caption(selected_description)
        
        st.line_chart(ts_df,x="Period", x_label="Period",y='Value', y_label=selected_name)
        st.dataframe(ts_df,use_container_width=True)
        

    if selected == "Home":

        st.title("SARB Market & Exhange Rates", help="https://custom.resbank.co.za/SarbWebApi/Help")

        # define various rate dataframes 
        capital_market_rates_df = df[df["SectionName"] == "Capital Market Rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        inflation_rates_df = df[df["SectionName"] == "Inflation rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        interest_rates_df = df[df["SectionName"] == "Interest rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        exchange_rates_df = df[df["SectionName"] == "Exchange rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]
        money_market_rates_df = df[df["SectionName"] == "Money Market Rates"][["Name", "Value", "Date", "UpDown","TimeseriesCode"]]

    
        st.caption("Trends", help="Movement: ▲ for up, ▼ for down, = for no change")

        # first container, with Interest, Inflation and Capital Market Rates
        with st.container():
            col1, col2, col3 = st.columns([1,1,3])
            with col1:
                st.subheader("Interest Rates", divider="green")
                for index, row in interest_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True, help=row['TimeseriesCode'])
                    
            with col2:
                st.subheader("Inflation Rates", divider="blue")
                for index, row in inflation_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True, help=row['TimeseriesCode'])

            with col3:
                st.subheader("Capital Market Rates", divider="violet")
                for index, row in capital_market_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True, help=row['TimeseriesCode'])

        # second container with Money Market and Exchange Rates
        with st.container():
            col1, col2, = st.columns([2,3])
            
            with col1:
                st.subheader("Money Market Rates", divider="red")
                for index, row in money_market_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True, help=row['TimeseriesCode'])
                
            with col2:
                st.subheader("Exchange Rates", divider="orange")
                # st.table(money_market_rates_df) #,hide_index=False)
                for index, row in exchange_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>R {row['Value']}</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True, help=row['TimeseriesCode'])

        # last container with raw data in table/dataframe
        with st.container():
                
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
                    format="DD-MM-YYYY",  # Custom date format
                    help="The date associated with the rate. dd-mm-yyyy",
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

except Exception as err:
    raise err 


