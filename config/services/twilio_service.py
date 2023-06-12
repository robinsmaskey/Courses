from django.conf import settings
from twilio.rest import Client


class TwilioSMSClient:
    def __init__(self) -> None:
        self.twilio_sid = settings.TWILIO_SID
        self.twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        self.twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    def get_client(self):
        client = Client(self.twilio_sid, self.twilio_auth_token)
        return client

    def send_sms(self, receiver_number, message_body):
        client = self.get_client()
        message = client.messages.create(
            from_=self.twilio_phone_number, to=receiver_number, body=message_body
        )
        return message.sid
