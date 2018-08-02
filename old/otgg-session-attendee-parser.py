#!/usr/local/bin/python

import csv

email_body = ""
with open('email-body.txt', 'r') as myfile:
    email_body = myfile.read()

with open('attendees.csv', 'rb') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',')

    location = ""
    session = ""
    for row in linereader:
    
        if row[0] == "Location":
            continue
    
        if (location != row[0]) or (session !=row[1]):
            location = row[0]
            session = row[1]
            
            print "One Team Gov Global update for attendees of discussion room", location, "during", session
            
            email_body = email_body.replace("<stuff>", "stuffish")
            email_body = email_body.replace("<things>", "thingish")

            print email_body
            
            print "To :", row[3]
        else:
            print row[3]


DON'T FORGET TO ADD IN THE VOLUNTEERS!