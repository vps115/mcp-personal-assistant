from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
    creds = None
    print('Checking for existing credentials...')
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If no (valid) credentials, let user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print('Error refreshing token. Removing token.json and requesting new authentication...')
                    if os.path.exists('token.json'):
                        os.remove('token.json')
                    creds = None
            
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'google_calendar_credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)
    except Exception as e:
        if os.path.exists('token.json'):
            os.remove('token.json')
        raise Exception(f"Authentication failed. Please try again. Error: {str(e)}")

# ========== Calendar CRUD ==========

def create_event(title, start_iso, end_iso, location=None, description=None):
    service = get_service()
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {'dateTime': start_iso, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_iso, 'timeZone': 'Asia/Kolkata'},
    }
    created_event = service.events().insert(calendarId='primary', body=event).execute()
    return created_event['id']

def list_events_for_date(start_date: str, end_date: str = None):
    """
    List events between start_date and end_date (inclusive).
    If end_date is not provided, only get events for start_date.
    """
    service = get_service()
    
    if end_date is None:
        end_date = start_date
        
    start = f"{start_date}T00:00:00+05:30"
    end = f"{end_date}T23:59:59+05:30"
    
    events_result = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])

def delete_event(event_id: str):
    service = get_service()
    service.events().delete(calendarId='primary', eventId=event_id).execute()

def update_event(event_id, **kwargs):
    service = get_service()
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    for key, value in kwargs.items():
        if key in ['summary', 'location', 'description']:
            event[key] = value
    updated_event = service.events().update(calendarId='primary', eventId=event_id, body=event).execute()
    return updated_event
