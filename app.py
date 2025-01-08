""" Simple application to fetch SARB Market Rates from SARB API and display.
"""

import streamlit as st
from sarb_api import sarb
from sarb_api import utils

def get_data():

    rates_data = sarb.fetch_all_rates()
    df_rates = sarb.convert_data_to_dataframe(rates_data)
    df_view = df_rates[["SectionName", "SectionId", "Name", "Value", "Date"]]
    
    return df_view

def get_capital_market_rates(df):
    """ 
    Return only the capital market rates from the given dataframe
    """

    try:
        capital_market_rates = df[df["SectionName"] == "Capital Market Rates"]

    except Exception as err:
        raise err 

def main():
  

    # setup landing page
    st.set_page_config(
        page_title="SARB Market and Exchange Rates"
        , page_icon=":shark:"
        , layout="wide"
        )
    # st.sidebar.image("./images/logo.jpg", width=100)
    st.sidebar.header("SARB Market and Exhange Rates")
  
    #popluate data
    df = get_data()

    # get various rates 
    capital_market_rates_df = df[df["SectionName"] == "Capital Market Rates"][["Name", "Value", "Date"]]
    inflation_rates_df = df[df["SectionName"] == "Inflation rates"][["Name", "Value", "Date"]]
    interest_rates_df = df[df["SectionName"] == "Interest rates"][["Name", "Value", "Date"]]
    exchange_rates_df = df[df["SectionName"] == "Exchange rates"][["Name", "Value", "Date"]]
    money_market_rates_df = df[df["SectionName"] == "Money Market Rates"][["Name", "Value", "Date"]]

    with st.container():
        col1, col2, col3 = st.columns([1,1,3])
        with col1:
            st.subheader("Interest Rates", divider="green")
            # st.dataframe(interest_rates_df,hide_index=False)
            for index, row in interest_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name} :  <strong>{row['Value']}%</strong></li>
                """, unsafe_allow_html=True)
                
        with col2:
            st.subheader("Inflation Rates", divider="blue")
            # st.dataframe(inflation_rates_df) #,hide_index=False)
            for index, row in inflation_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name} :  <strong>{row['Value']}%</strong></li>
                """, unsafe_allow_html=True)

        with col3:
            st.subheader("Capital Market Rates", divider="red")
            # st.table(capital_market_rates_df) #,hide_index=False)
            for index, row in capital_market_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name.upper()} :  <strong>{row['Value']}%</strong></li>
                """, unsafe_allow_html=True)

    with st.container():
        col1, col2, = st.columns([2,3])
        
        with col1:
            st.subheader("Money Market Rates", divider="violet")
            # st.table(money_market_rates_df) #,hide_index=False)
            for index, row in money_market_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name} :  <strong>{row['Value']}%</strong></li>
                """, unsafe_allow_html=True)

        with col2:
            st.subheader("Exchange Rates", divider="grey")
            # st.table(money_market_rates_df) #,hide_index=False)
            for index, row in exchange_rates_df.iterrows():
                name :str = row["Name"]
                st.markdown(f"""
                    <li font-size:18px;">{name} :  <strong>R {row['Value']}</strong></li>
                """, unsafe_allow_html=True)

    st.write("---")

    with st.container():
        st.subheader("Data Grid")
        st.dataframe(df, use_container_width=True)

    if st.sidebar.button("Refresh Data"):
        st.rerun()  # This reloads the page
    
    st.sidebar.download_button(
        label="Save to CSV",
        data=df.to_csv(),
        file_name="sars_data.csv",
        mime="text/csv"
    )
        
   
if __name__ == "__main__":
     main()


