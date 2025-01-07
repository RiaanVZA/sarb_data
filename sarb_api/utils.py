import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import os

def save_as_csv(df, file_name, email:bool=False):
    """ Save the contents of a dataframe to a CSV file.
    """
       
    try:

        # create a sub section (view)
        df_view = df[["SectionName", "Name", "Value", "Date"]]
        file_path = f"./uncommitted/{file_name}.csv"

        if os.path.exists(file_path):
            os.remove(file_path)

        df_view.to_csv(file_path)

        if email == True:
            send_email("riaanv@sahomeloans.com",file_path)

    except Exception as err:
        raise err 


def send_email(to_addresses, file_path):
    # Sender's email credentials
    sender_email = "riaanvermeulen@gmail.com"
    sender_password = "rvxthzgrqleqnpgd"
    subject = "Daily Rates from SARB."
    body = "Good day, herewith your daily Rates provided by the South African Reserve Bank. Regards Riaan." 


    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ", ".join(to_addresses)  # List of recipients
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # Attach the CSV file
    attachment = open(file_path, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(file_path)}")

    # Attach the part to the message
    msg.attach(part)

    # Establish a secure session with Gmail's SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            text = msg.as_string()
            server.sendmail(sender_email, to_addresses, text)
            print("Email successfully sent!")
    except Exception as e:
        print(f"Failed to send email: {e}")