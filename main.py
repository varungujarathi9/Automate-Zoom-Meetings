'''
### Description
    - I have developed this application so that one need not worry about the logistics of meeting and stay focused on his/her work
    - This python application automatically reads Zoom meetings from Google Calendar and starts the meetings 10 min before the time

### Author
Varun Gujarathi

### Created On
06th Sept 2020

### References
https://github.com/prashanth-up/Zoom-Automation/blob/master/main.py
https://developers.google.com/calendar/quickstart/python
'''
from __future__ import print_function
import datetime
import pickle
import os.path
import pyautogui
import schedule
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

meetings = {}


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('.credentials/token.pickle'):
        with open('.credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('.credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        startTime = event['start'].get('dateTime', event['start'].get('date'))

        # get the meeting ID
        meetingIDIndexStart = int(event['description'].find('Meeting ID:'))
        meetingIDIndexEnd = meetingIDIndexStart + len('Meeting ID:')
        meetingIDStarted = False
        meetingIDExists = False
        meetingID = ''
        while True:
            # read only number occuring after meetingIDIndexEnd
            meetingIDIndexEnd += 1
            nextOccurringCharacter = event['description'][meetingIDIndexEnd]
            if nextOccurringCharacter.isnumeric():
                meetingIDStarted = True
                meetingID += nextOccurringCharacter

            elif nextOccurringCharacter is '\n' and meetingIDStarted is True:
                break

        if meetingID is not '':
            meetingIDExists = True
            meetingID = int(meetingID)

        # getting meeting password
        meetingPasswordIndexStart = int(event['description'].find('Passcode:'))
        meetingPasswordIndexEnd = meetingPasswordIndexStart + len('Passcode:')
        meetingPasswordStarted = False
        meetingPasswordExists = False
        meetingPassword = ''
        while True:
            # read only alphanumeric occuring after meetingPasswordIndexEnd
            meetingPasswordIndexEnd += 1
            nextOccurringCharacter = event['description'][meetingPasswordIndexEnd]
            if nextOccurringCharacter.isalnum():
                meetingPasswordStarted = True
                meetingPassword += nextOccurringCharacter

            elif nextOccurringCharacter is '\n' and meetingPasswordStarted is True:
                break

        if meetingIDExists is True:
            meetings[event['summary']] = {'Time':startTime, 'Meeting ID': meetingID, 'Password':meetingPassword}

if __name__ == '__main__':
    main()
    print(meetings)