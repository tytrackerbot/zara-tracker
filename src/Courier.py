from zara import ZaraItem
import os
import smtplib
import imghdr
from email.message import EmailMessage
import jsonpickle

mail_address = os.environ.get('MAIL_USERNAME')
mail_password = os.environ.get('MAIL_PASSWORD')
receiver_address = os.environ.get('RECEIVER_USERNAME')

# Set Mail Credentials
msg = EmailMessage()
msg['Subject'] = 'ZARA SMALL AVAILABLE !!!'
msg['From'] = mail_address
msg['To'] = receiver_address

# Obtain Item
data_file = os.path.dirname(os.path.abspath(
    __file__)) + os.path.sep + os.path.join('..', 'data', 'data.json')

with open(data_file, 'r') as file:
    content = file.read()
    item = jsonpickle.decode(content)

if item.mail_count < 3 and item.isSmallSizeAvailable():
    # Update Item
    item.mail_count += 1
    item.saveToJSON(data_file)

    # Generate Mail
    msg.add_alternative(f'''\
        <!DOCTYPE html>
        <html>
            <body>
                <h3>Zara Small Available</h3>
                <a href="{item.url}">Visit Website</a> 
            </body>
        </html>
        ''', subtype='html')

    # Send mail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(mail_address, mail_password)
        smtp.send_message(msg)
