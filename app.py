""" Simple application to fetch SARB Market Rates from SARB API and display.
"""

import streamlit as st
from sarb_api import sarb

def get_api_data():

    rates_data = sarb.fetch_all_rates()
    df_rates = sarb.convert_data_to_dataframe(rates_data)
    df_view = df_rates[["SectionName", "SectionId", "Name", "Value", "UpDown", "Date"]]
    
    return df_view

def map_updown(change: int):

    if change == 1:
        return '<span style="color:green;"> ▲ </span>'  # Up arrow
    elif change == 0: 
        return '<span style="color:gray;"> = </span>'  # No change
    elif change == -1: 
        return '<span style="color:red;"> ▼ </span>'  # Down arrow
    else:
        return ''

def main():
  
    try:

        # fetch data from SARB APIs
        df = get_api_data()

        # setup landing page
        st.set_page_config(
            page_title="SARB Market and Exchange Rates"
            , page_icon=":chart_with_upwards_trend:"
            , layout="wide"
            )

        # setup sidebar
        st.sidebar.header("SARB Market and Exhange Rates")
        st.sidebar.caption("https://custom.resbank.co.za/SarbWebApi/Help")
        if st.sidebar.button("Refresh API Data"):
            st.rerun()  # This reloads the page
        st.sidebar.download_button(
            label="Save to CSV",
            data=df.to_csv(),
            file_name="sars_data.csv",
            mime="text/csv"
        )

        # define various rate dataframes 
        capital_market_rates_df = df[df["SectionName"] == "Capital Market Rates"][["Name", "Value", "Date", "UpDown"]]
        inflation_rates_df = df[df["SectionName"] == "Inflation rates"][["Name", "Value", "Date", "UpDown"]]
        interest_rates_df = df[df["SectionName"] == "Interest rates"][["Name", "Value", "Date", "UpDown"]]
        exchange_rates_df = df[df["SectionName"] == "Exchange rates"][["Name", "Value", "Date", "UpDown"]]
        money_market_rates_df = df[df["SectionName"] == "Money Market Rates"][["Name", "Value", "Date", "UpDown"]]

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
                    """, unsafe_allow_html=True)
                    
            with col2:
                st.subheader("Inflation Rates", divider="blue")
                for index, row in inflation_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True)

            with col3:
                st.subheader("Capital Market Rates", divider="violet")
                for index, row in capital_market_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True)

        # second container with Money Market and Exchange Rates
        with st.container():
            col1, col2, = st.columns([2,3])
            
            with col1:
                st.subheader("Money Market Rates", divider="red")
                for index, row in money_market_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>{row['Value']}%</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True)
                
            with col2:
                st.subheader("Exchange Rates", divider="orange")
                # st.table(money_market_rates_df) #,hide_index=False)
                for index, row in exchange_rates_df.iterrows():
                    name :str = row["Name"]
                    st.markdown(f"""
                        <li font-size:18px;">{name}: <strong>R {row['Value']}</strong>{map_updown(row['UpDown'])}</li>
                    """, unsafe_allow_html=True)

        

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
            }

            df["UpDown"] = df["UpDown"].map(arrow_mapping)
            st.dataframe(df, use_container_width=True, hide_index=True, column_config=column_config)

    except Exception as err:
        raise err 
   
if __name__ == "__main__":
     main()


