import os


EMAIL_USE_TLS=True
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_HOST_USER=os.environ.get('Sender_email')
EMAIL_HOST_PASSWORD=os.environ.get('Sender_password')
EMAIL_PORT=587