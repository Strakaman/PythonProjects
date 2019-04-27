# Python3 only
# Import smtplib for the actual sending function
import smtplib
import datetime
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

textfile = "test.txt"

FROMADDR = "" #replace with e-mail address
realPass = "" #replace with password
TOADDRS  = [""] #replace with list of recipients
LOGIN    = FROMADDR

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    # Create a text/plain message
    msg = EmailMessage()
    BODY = MIMEText(fp.read())
    msg.set_content(BODY)

# me == the sender's email address
# TOADDRS == the recipient's email address
now = datetime.datetime.now()
msg['Subject'] = 'Automated Email Yo ' + now.strftime("%Y/%m/%d-%H:%M")
msg['From'] = FROMADDR
msg['To'] = TOADDRS

# Send the message via our own SMTP server.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(1)
server.ehlo()
print(str(server.esmtp_features))
server.starttls()
server.login(LOGIN, realPass)
server.send_message(msg)
server.quit()