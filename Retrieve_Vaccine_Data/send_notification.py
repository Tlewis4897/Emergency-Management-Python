import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_test_change_notif(config, mismatch_list):
    try:
        # Loop over test change list, create email html
        ul = "<ul >"
        for test_changes in mismatch_list:
            ul += f"""<li> Change Found: {test_changes}</li>
            """
        ul += "</ul>"
        from_address = config["email_creds"]["from_email"]
        to_address = config["email_creds"]["to_emails"]
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Test email"
        msg['From'] = from_address
        msg['To'] = to_address
        # Create the message (HTML).
        html = ul
        # Record the MIME type - text/html.
        part1 = MIMEText(html, 'html')
        # Attach parts into message container
        msg.attach(part1)
        # Credentials
        username = config["email_creds"]["username"]
        password = config["email_creds"]["gmail_app_id"]
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_address, to_address,
                        msg.as_string())
        server.quit()
    except Exception as e:
        print(e)