from twilio.rest import Client
import random

def send_otp(phone_number):
    otp = ''.join(random.choices('0123456789', k=6))  # Generate 6-digit OTP
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    return otp
