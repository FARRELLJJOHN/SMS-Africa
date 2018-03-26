import os
from twilio.rest import Client

# Twilio Account Info

account_SID = 'AC0dc3742bf14eb1d1a3d0f90d48637f53'
auth_token = '96fcfbae92e874522d8d248e8226b35b'

client = Client(account_SID, auth_token)

# TODO: convert above to global variables or otherwise more secure form

def newMessage(toNumber, messageBody):

    numberString = str(toNumber)
    numberString.strip('()+-. ')
    numberString.replace(" ", "")
    if numberString[:2] != '+1':
        numberString = '+1{}'.format(numberString)

    client.messages.create(
        to=numberString,
        from_="+12028398525",
        body=str(messageBody)
    )
