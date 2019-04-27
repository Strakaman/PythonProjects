#Works with Python 2 and 3
import smtplib

FROMADDR = "" #replace with e-mail address
realPass = "" #replace with password
TOADDRS  = [""] #replace with list of recipients
LOGIN    = FROMADDR
BODY = "This is the body of the e-mail"

SUBJECT  = "Test Email Subject"

msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
       % (FROMADDR, ", ".join(TOADDRS), SUBJECT) )
msg += BODY + "\r\n"

server = smtplib.SMTP('smtp.gmail.com', 587) #replace accordingly with sender e-mail domain and port
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(LOGIN, realPass)
server.sendmail(FROMADDR, TOADDRS, msg)
server.quit()