import os
from twilio.rest import *


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def twilio_message(number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body='This is your Link',
            from_='+17406886883',
            to='+1{}'.format(number)
        )
    print(message.sid)

