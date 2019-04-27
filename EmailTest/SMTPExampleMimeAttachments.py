# Python3 only
# Import smtplib for the actual sending function
import smtplib
import datetime
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

textfile = "body.txt"

FROMADDR = "" #replace with e-mail address
realPass = "" #replace with password
TOADDRS  = [""] #replace with list of recipients
LOGIN    = FROMADDR

# Import the email modules we'll need
from email.message import EmailMessage

# Open the plain text file whose name is in textfile for reading.
with open(textfile) as fp:
    msg = MIMEMultipart() #message has multiple parts
    BODY = MIMEText(fp.read())
    msg.attach(BODY)

# me == the sender's email address
# TOADDRS == the recipient's email address
now = datetime.datetime.now()
msg['Subject'] = 'Automated Email Yo ' + now.strftime("%Y/%m/%d-%H:%M")
msg['From'] = FROMADDR
msg['To'] = ", ".join(TOADDRS)

#attachments
f = open("test.txt")
attachment = MIMEText(f.read())
#this line indicates other MIME parts are attachments
attachment.add_header('Content-Disposition', 'attachment', filename="test.txt") 
msg.attach(attachment)

img_data = open('fire.png', 'rb').read()
img = MIMEImage(img_data, 'png',name="RandomFire")
msg.attach(img)

# Send the message via our own SMTP server.
server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(1)
server.ehlo()
print(str(server.esmtp_features))
server.starttls()
server.login(LOGIN, realPass)
server.send_message(msg)
server.quit()