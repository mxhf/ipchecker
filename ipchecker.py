#!/usr/bin/env python
import requests
import logging
import time
from datetime import datetime
from threading import Thread

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

PERIODICAL_CHECK_INTERVAL = 3600


def send_email(alert_summary, info = "" ):
    global EMAIL_SENT
    
    COMMASPACE = ', '

    gmail_user = 'mxhfesp32@gmail.com'  
    gmail_password = 'Dtnc4ui8QGQh'

    sent_from = gmail_user  
    to = ['mfabricius@gmail.com']  
    subject = alert_summary

    email_text  = "{}\n".format(alert_summary)
    email_text += "{}\n".format(info)
    
    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = COMMASPACE.join(to)
    part1 = MIMEText(email_text, 'plain')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    
    
    try: 
        logger.info("send_email: Trying to send email.")
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, msg.as_string())
        server.close()

        logger.info( 'send_email: Email sent!' )
    except:  
        logger.error( 'send_email: Something went wrong...' )


def periodical_check():
    global PERIODICAL_CHECK_INTERVAL
    while True:
      logger.info("periodical_check: Checking")
      ip = requests.get('https://checkip.amazonaws.com').text.strip()
      logger.info('periodical_check: ip is {}'.format(ip))

      logger.info("periodical_check: Sending warning email.")
      send_email("IP is: {}".format(ip))
                          
      time.sleep(PERIODICAL_CHECK_INTERVAL)



# create logger with 'spam_application'
logger = logging.getLogger('ipchecker')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('/var/log/ipchecker.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# 'application' code
logger.debug('Start ipchecker')

if __name__ == '__main__':
  thread = Thread(target=periodical_check)
  thread.deamon = True
  thread.start()

