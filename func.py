import json
import os
import pickle
from inspect import getmembers
from pprint import pprint

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def var_dump(obj: object) -> None:
    """
    Print var_dump alternative

    :return: None
    :rtype: None
    """
    pprint(getmembers(obj))
    return None


def payload():
    """
    Return dict if json file exist.


    May cause an exception if the environment variable is not set.
    :return: dict with keys for request
    :rtype: dict
    """
    if os.path.exists('payload.json'):
        with open('payload.json', 'r') as key_file:
            return json.load(key_file)
    else:
        return {'key': os.environ['SHEET_KEY']}


def get_cred():
    """
    Create connection to google calendar.

    Put cr.json into project root. May cause an exception if the environment variable is not set.
    :return: connection to google calendar
    :rtype: object
    """
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    cr_json = {
            "installed": {
                    "project_id": "spread2cal",
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    }
            }
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
            #
            if os.path.exists('cr.json'):
                with open('cr.json', 'r') as cr:
                    keys = json.load(cr)
                    for v in keys['installed']:
                        cr_json['installed'][v] = keys['installed'][v]
            else:
                cr_json['installed']['client_id'] = os.environ['CLIENT_ID']
                cr_json['installed']['client_secret'] = os.environ['CLIENT_SECRET']
                cr_json['installed']['redirect_uris'] = os.environ['REDIRECT_URIS']

            with open('credentials.json', 'w') as file:
                json.dump(cr_json, file)
            #
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def decorator(func):
    """
    Simple decorator.

    Print function name.

    :param func: your function
    :type func: object
    :return: your function
    :rtype: object
    """

    def pre(*args):
        print('run: ', func.__name__)
        func(*args)

    return pre
