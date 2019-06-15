from __future__ import print_function
import datetime
from dateutil.parser import parse
from datetime import timezone
import pytz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events', 
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar'
]


def synchronize(schedule, calendarname = "Schedule from Python Program"):
    
    if os.path.exists('schedule.pickle'):
        with open('schedule.pickle', 'rb') as schedule_pickle:
            old_schedule = pickle.load(schedule_pickle)
            if old_schedule != schedule:
                print('Schedule is changed')
            else:
                print('Schedule is stable')
    else:
        print('First sync')       

    with open('schedule.pickle', 'wb') as schedule_pickle:
        pickle.dump(schedule, schedule_pickle)



    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow()
    print('Getting the upcoming 10 or less events')
    
    calendars_list = {}
    
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            calendars_list[calendar_list_entry['summary']] = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    if not calendars_list.get(calendarname):
        r = service.calendars().insert(body={"summary": calendarname,"timeZone": "Europe/Warsaw"}).execute()
        calendarid = r['id']
    else:
        calendarid = calendars_list[calendarname]

    events_result = service.events().list(calendarId=calendarid, timeMin=now.isoformat()+'Z', singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    else:
        print('Clear previous events')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        service.events().delete(calendarId=calendarid, eventId=event['id']).execute()

    print('Create new events')
    
    now = datetime.datetime.now()

    color_map = {
        'LE': '11',
        'E': '5',
        'L': '2',
        'S': '7'
    }

    for row in schedule.get_body():
        start_date = "%sT%s:00" % (row['date'], row['from'],)
        end_date = "%sT%s:00" % (row['date'], row['to'],)
        
        subject_start_at = parse(start_date)

        if subject_start_at < now:
            continue
            
        event = {
            'summary': "%s | %s: %s" % (row['type'], row['classroom'], row['subject'],),
            'location': row['location'],
            'description': '<b>Teacher:</b> %s <br>%s <br><b>%s</b>' % (row['teacher'], row['description'],row['submit'],),
            'start': {
                'dateTime': start_date,
                'timeZone': 'Europe/Warsaw'
            },
            'end': {
                'dateTime': end_date, #'2019-03-16T16:30:00+01:00',
                'timeZone': 'Europe/Warsaw'
            },
            'reminders': {
                'useDefault': False
            },
            'colorId': color_map.get(row['type'], '0')
        }
        service.events().insert(calendarId=calendarid, body=event).execute()

if __name__ == '__main__':
    synchronize()