# Automate-Zoom-Meetings

## Python application to automatically join meetings scheduled on Google Calendar

WHY - While 'Work From Home' has become a norm, many of us use 'Zoom Meetings' platform meetings an stuff. As a developer I used to lose track of time and forget about these meeting that were scheduled by my manager. Also it seems productive to focus on the work at hand rather than stressing about meeting timing and when to join and when to not. Thus automating the stuff.

HOW - The application reads events from your Google Calendar, filters out 'Zoom' events, then extracts all the relative information and stores it. Now whenever a meeting is scheduled for a particular date & time, the application opens Zoom App, enter meeting ID & password and joins the meeting 10 mins before the start time.

## Requirements

- [x] Installed python version above 3.5
- [x] Updated Zoom Software (Signed in)

## Steps

### Enable the Google Calendar API and download the client credentials file

Follow the instruction on this link - <https://developers.google.com/calendar/quickstart/python>
Download the credentials.json file and keep it inside .credentials folder

### Install the Python libraries

Install libraries from requirements.txt

### Run application

python main.py

### Connect to your Google calendar

When you start the application for first time, it would throw out a link in CLI, go to that link and authenticate
