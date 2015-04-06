import smtplib

from config import Config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Emailer():

    def __init__(self):
        pass

    def send_mail(self, subject, text, is_gmail=False):
        msg = self._compose_mail(subject, text)
        if is_gmail:
            self._send_email_via_gmail(self, msg)
        else:
            self._send_email_via_localhost(self, msg):

    def _compose_mail(subject, text):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = Config.FROM
        msg['To'] = ", ".join(Config.TO_LIST)
        part = MIMEText(text, 'html')
        msg.attach(part)
        return msg

    def _send_email_via_gmail(self, msg):
        try:
            server = smtplib.SMTP(Config.SMTP_GMAIL, Config.PORT_GMAIL)
            server.ehlo()
            server.starttls()
            server.login(Config.FROM, Config.PASSWD)
            server.sendmail(Config.FROM, Config.TO_LIST, msg.as_string())
            server.close()
            print 'successfully sent the mail'
        except Exception, e:
            print "failed to send mail", e

    def _send_email_via_localhost(self, msg):
        try:
            server = smtplib.SMTP(Config.SMTP)
            server.sendmail(Config.FROM, Config.TO_LIST, msg.as_string())
            server.close()
            print 'successfully sent the mail'
        except Exception, e:
            print "failed to send mail", e
