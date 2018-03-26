import os
from twilio.rest import Client

# Twilio Account Info

account_SID = '****************************'
auth_token = '**************************'

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
