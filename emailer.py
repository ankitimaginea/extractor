import smtplib

from config import Config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer():

    def __init__(self):
        pass

    def send_email(self, subject, text):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Config.FROM
        msg['To'] = ", ".join(Config.TO_LIST)
        part = MIMEText(text, 'html')
        msg.attach(part)
        try:
            server = smtplib.SMTP(Config.SMTP, Config.PORT)
            server.ehlo()
            server.starttls()
            server.login(Config.FROM, Config.PASSWD)
            server.sendmail(Config.FROM, Config.TO_LIST, msg.as_string())
            server.close()
            print 'successfully sent the mail'
        except Exception, e:
            print "failed to send mail", e
