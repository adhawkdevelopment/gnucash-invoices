from googleapiclient.discovery import build
from apiclient import errors
import base64
from google.oauth2 import service_account
from email.message import EmailMessage
from email.mime.image import MIMEImage



EMAIL_FROM = ''
EMAIL_CONTENT = ''


def create_message(email_to, email_subject, attachment):
    

    message = EmailMessage()

    message.set_content(EMAIL_CONTENT)
    
    message['to'] = email_to
    message['from'] = EMAIL_FROM
    message['subject'] = email_subject

    # attachment
    maintype = 'application'
    subtype = 'pdf'

    with open(attachment, "rb") as fp:
        attachment_data = fp.read()
        message.add_attachment(attachment_data, maintype, subtype, filename=email_subject)

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except errors.HttpError as error:
        print('gmail.send_message(service, user_id, message)')
        print('An error occurred: %s' % error)
        return None


def service_account_login():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    SERVICE_ACCOUNT_FILE = 'service-key.json'
    credentials = service_account.Credentials.from_service_account_file(__path__[0] + "/" + SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    delegated_credentials = credentials.with_subject(EMAIL_FROM)
    service = build('gmail', 'v1', credentials=delegated_credentials)
    return service



def sendMail(email_to, email_subject, attachment):
    service = service_account_login()
    message = create_message(email_to, email_subject, attachment)
    send_message(service, EMAIL_FROM, message)
