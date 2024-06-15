import requests

# Mailjet API credentials
API_KEY = '6541ab6a282e40b21f028b34d928d82a'
API_SECRET = '739ec61baccbf328f4f022dff224808d'

# Mailjet API endpoint
MAILJET_API_URL = 'https://api.mailjet.com/v3.1/send'

# Sender and recipient details
sender_email = 'rajendra44prasad@gmail.com'
recipient_email = 'rajubabu1610@gmail.com'
subject = 'Test Email from Mailjet'
body = 'Hello, this is a test email sent from Mailjet API.'

# Mailjet API request payload
payload = {
    'Messages': [
        {
            'From': {
                'Email': sender_email,
                'Name': 'Sender Name'
            },
            'To': [
                {
                    'Email': recipient_email,
                    'Name': 'Recipient Name'
                }
            ],
            'Subject': subject,
            'TextPart': body,
            'HTMLPart': '<p>' + body + '</p>'
        }
    ]
}

# Send the email via Mailjet API
try:
    response = requests.post(MAILJET_API_URL, auth=(API_KEY, API_SECRET), json=payload)
    response.raise_for_status()  # Raise exception for HTTP errors
    print('Email sent successfully.')
except requests.exceptions.HTTPError as e:
    print(f'Error sending email: {e}')
