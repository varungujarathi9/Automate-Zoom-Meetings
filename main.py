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

#### TO-DO
1. Check if app is already running
2. Check if the person has responded yes to the meeting
3. Read whether the event for Zoom only
4. Add support for other platforms too
5. Add support for iCalendar
'''
from __future__ import print_function
import datetime
import time
import pytz
import pickle
import subprocess
import os.path
import os
import pyautogui
import schedule
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

meetings = {}


def getCalendarEvents():
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
        startTimeStr = (event['start'].get('dateTime', event['start'].get('date')))[:-6]
        descLength = len(event['description'])
        # get the meeting ID
        meetingIDIndexStart = int(event['description'].find('Meeting ID:'))
        meetingIDIndexEnd = meetingIDIndexStart + len('Meeting ID:')
        meetingIDStarted = False
        meetingIDExists = False
        meetingID = ''
        while meetingIDIndexEnd < descLength:
            # read only number occuring after meetingIDIndexEnd

            nextOccurringCharacter = event['description'][meetingIDIndexEnd]
            meetingIDIndexEnd += 1
            if nextOccurringCharacter.isnumeric():
                meetingIDStarted = True
                meetingID += nextOccurringCharacter

            elif nextOccurringCharacter is '<' and meetingIDStarted is True:
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

        while meetingPasswordIndexEnd < descLength:
            # read only alphanumeric occuring after meetingPasswordIndexEnd

            nextOccurringCharacter = event['description'][meetingPasswordIndexEnd]
            meetingPasswordIndexEnd += 1
            if nextOccurringCharacter.isalnum():
                meetingPasswordStarted = True
                meetingPassword += nextOccurringCharacter

            elif nextOccurringCharacter is '\n' and meetingPasswordStarted is True:
                break

        # getting meeting link
        #  try to get link from 'location' key
        if event['location'] is not None:
            meetingLink = event['location']
        else:
            joinTextStart = int(event['description'].find('Join'))
            meetingLinkIndexStart = int(event['description'].find('http', joinTextStart, -1))
            # meetingLinkIndexEnd = meetingLinkIndexStart + len('http') + 13
            meetingLinkStarted = False
            meetingLinkExists = False
            meetingLink = ''

            # print(event['description'])

            while meetingLinkIndexStart < meetingIDIndexStart:
                # read only alphanumeric occuring after meetingLinkIndexEnd

                nextOccurringCharacter = event['description'][meetingLinkIndexStart]
                meetingLinkIndexStart += 1
                if nextOccurringCharacter == '<':
                    while event['description'][meetingLinkIndexStart] != '>':
                        meetingLinkIndexStart += 1
                    meetingLinkIndexStart += 1
                elif nextOccurringCharacter == '"' and meetingLinkStarted is True:
                    break
                else:
                    meetingLinkStarted = True
                    meetingLink += nextOccurringCharacter

        if meetingIDExists is True:
            meetings[event['summary']] = {'Time':datetime.datetime.strptime(startTimeStr, '%Y-%m-%dT%H:%M:%S'), 'Meeting ID': meetingID, 'Link':meetingLink, 'Password':meetingPassword}

    print(meetings.keys())

def startZoomCall(meetingID, meetingPassword):

    # open zoom app
    time.sleep(0.2)
    os.popen('zoom')
    time.sleep(10)

    # find the Join Meeting button
    x,y = pyautogui.locateCenterOnScreen('res/JoinMeeting.png',confidence = 0.8, grayscale=False)
    pyautogui.click(x,y)
    time.sleep(2)

    # find the Meeting ID field
    x,y = pyautogui.locateCenterOnScreen('res/MeetingID.png',confidence = 0.8, grayscale=False)
    pyautogui.click(x,y)
    time.sleep(2)

    # enter the meeting link
    pyautogui.write(str(meetingID))
    time.sleep(2)

    # click on the Join button
    x,y = pyautogui.locateCenterOnScreen('res/JoinButton.png',confidence = 0.8, grayscale=False)
    pyautogui.click(x,y)
    time.sleep(2)

    # enter the password 
    pyautogui.write(meetingPassword)
    pyautogui.press('enter',interval = 10)

if __name__ == '__main__':
    getCalendarEvents()
    dateTimeNow = None
    while True:
        schedule.every().hour.do(getCalendarEvents)
        time.sleep(1)
        print(meetings)
        print(dateTimeNow)
        finalMeetings = meetings.copy()
        for meetingName, meetingData in finalMeetings.items():
            dateTimeNow = datetime.datetime.strptime(datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%dT%H:%M'), '%Y-%m-%dT%H:%M')
            dateTimeNow = dateTimeNow + datetime.timedelta(minutes = 10)
            if meetingData['Time'] <= dateTimeNow:
                print(meetingData['Link'])
                startZoomCall(meetingData['Link'], meetingData['Password'])
                del meetings[meetingName]