#!/usr/bin/python3.4
import smtplib
from email.mime.text import MIMEText

msg = MIMEText("The body of the email is here")
msg['Subject'] = "An Email Alert"
msg['From'] = "ryan@pythonscraping.com"
msg['To'] = "g.urbano.ma@gmail.com"
s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

