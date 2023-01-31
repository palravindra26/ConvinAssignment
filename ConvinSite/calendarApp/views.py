from __future__ import print_function

from django.shortcuts import render, redirect
from django.http import HttpResponse

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def home(request):
    return render(request, 'index.html')


def GoogleCalendarInitView(request):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return redirect(GoogleCalendarRedirectView)


def GoogleCalendarRedirectView(request):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 25 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=25, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return HttpResponse('No upcoming events found.')

        return render(request, 'events.html', {'events': events})

    except HttpError as error:
        print('An error occurred: %s' % error)
