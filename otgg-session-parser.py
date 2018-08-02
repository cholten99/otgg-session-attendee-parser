# Imports

# For Gmail
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from email.mime.text import MIMEText
import base64
from googleapiclient import errors

# For debugging
import sys

# For CSV reader
import csv

# MAIN

# Initialise the Gmail API
SCOPES = 'https://www.googleapis.com/auth/gmail.compose'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

# Read in template email body

email_template_handle = open("email_template.txt", "r")
email_template = email_template_handle.read()

# Read in session docs CSV

session_docs_file_handle = open("session_docs.csv", "r")
session_docs_reader = csv.reader(session_docs_file_handle)
session_docs_list = []
for row in session_docs_reader:
  session_docs_list.append([ row[0], row[1], row[2], row[3] ])

# Read in attendee CSV

all_attendees_file_handle = open("all_attendees.csv", "r")
all_attendees_reader = csv.reader(all_attendees_file_handle)
all_attendees_dict = {}
for row in all_attendees_reader:
  all_attendees_dict[row[0].strip().lower()] = row[1]

# Read in session attendance CSV

session_attendees_file_handle = open("session_attendees.csv", "r")
session_attendees_reader = csv.reader(session_attendees_file_handle)
session_attendees_list = []
for row in session_attendees_reader:
  session_attendees_list.append([ row[0], row[1], row[2], all_attendees_dict[row[2].strip().lower()] ])

# Loop through sessions and locations
for session_row in session_docs_list:

  # For each new pairing map into the template email body
  session = "Session " + session_row[0]
  location = session_row[1]
  doc = session_row[2]

  # Create a list of email addresses for people who went to session
  email_to_list = []
  for session_attendee in session_attendees_list:
    if ( (session_attendee[0] == location) and (session_attendee[1] == session) ):
      email_to_list.append(session_attendee[3])

  # Map info into email template
  message_body = email_template
  message_body = message_body.replace("<location>", location)
  message_body = message_body.replace("<session>", session.lower())
  message_body = message_body.replace("<session-notes-doc>", doc)

  # Use list of email addresses to send to everyone
  message = MIMEText(message_body)
  subject = "One Team Gov Global follow-up : " + location + " " + session.lower()
  message['subject'] = subject

  # Set up to and from
  message['from'] = "dave@bowsy.co.uk"
  to_list = ""
  for email_address in email_to_list:
    to_list = to_list + email_address + ","
  to_list = to_list[:-1]

  # Skip if no-one is recorded as going
  if (to_list == ""):
    continue
  else:
    message['to'] = to_list

  # Send it off
  message = {'raw': base64.urlsafe_b64encode(message.as_string())}
  try:
    ret_val = service.users().messages().send(userId="me", body=message).execute()
    print('Message Id: %s' % ret_val['id'])
  except errors.HttpError, error:
    print('An error occurred: %s' % error)
