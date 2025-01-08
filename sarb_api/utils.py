import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
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


def send_email():
    # Sender's email credentials
    sender_email = "riaanvermeulen@gmail.com"
    custom_sender = "no-reply@sahomeloans.com"
    recipient_email = "riaanv@sahomeloans.com"
    sender_password = "rvxthzgrqleqnpgd"
    subject = "Daily Rates from SARB."
    body = "<body><p>Good day.</p><p>Attached your daily rates as provided by the South African Reserve Bank.</p><p>Regards Riaan.</p>"


    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = custom_sender
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'html'))

    # Attach the CSV files
    home_page_rates_file = "./uncommitted/home_page_rates.xlsx"
    current_market_rates_file = "./uncommitted/current_market_rates.xlsx"
    historical_exchange_rates_file = "./uncommitted/historical_exchange_rates_daily.xlsx"

    # home page rates
    if os.path.exists(home_page_rates_file):
        attachment = open(home_page_rates_file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(home_page_rates_file)}")
        msg.attach(part)

    # current market rates
    if os.path.exists(current_market_rates_file):
        attachment = open(current_market_rates_file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(current_market_rates_file)}")
        msg.attach(part)
   
    # daily exchange rates
    if os.path.exists(historical_exchange_rates_file):
        attachment = open(historical_exchange_rates_file, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(historical_exchange_rates_file)}")
        msg.attach(part)
    
    

    # Establish a secure session with Gmail's SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, recipient_email, text)
            server.quit()
            print("Email successfully sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")