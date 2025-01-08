import pandas as pd
import os

def save_as_csv(df, file_name):
    """ Save the contents of a dataframe to a CSV file.
    """
       
    try:

        # create a sub section (view)
        df_view = df[["SectionName", "Name", "Value", "Date"]]
        file_path = f"./uncommitted/{file_name}.csv"

        if os.path.exists(file_path):
            os.remove(file_path)

        df_view.to_csv(file_path)

    except Exception as err:
        raise err 

def save_as_xlsx(df, file_name):
    """ Save the contents of a dataframe to a CSV file.
    """
       
    try:

        # create a sub section (view)
        df_view = df[["SectionName", "Name", "Value", "Date"]]
        file_path = f"./uncommitted/{file_name}.xlsx"

        if os.path.exists(file_path):
            os.remove(file_path)

        df_view.to_excel(file_path)

    except Exception as err:
        raise err 