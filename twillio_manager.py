from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from config import ACCOUNT_SID, AUTH_TOKEN, TWILIO_NUMBER
import logging


def send_sms(to, body):
    """Sends an sms to the target phone number"""
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    try:
        message = client.messages.create(body=body,
                                         to=to,
                                         from_=TWILIO_NUMBER)
    except TwilioRestException:
        message = "Failed while sending message to: {to} with body: {body}".format(to=to, body=body)
        logging.exception(message)
    return message
