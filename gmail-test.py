#!/usr/bin/python

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
from googleapiclient import errors

# Setup the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Set up message
message = MIMEText("What a body!")
message['to'] = "dave@bowsy.co.uk,cholten99@gmail.com"
message['subject'] = "What a subject 3 : Sharknado"
message = {'raw': base64.urlsafe_b64encode(message.as_string())}

# Send
try:
  ret_val = service.users().messages().send(userId="me", body=message).execute()
  print('Message Id: %s' % ret_val['id'])
except errors.HttpError, error:
  print('An error occurred: %s' % error)
