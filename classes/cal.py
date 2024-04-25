from datetime import datetime as date

from func import get_cred


class Cal:
    """
    Calendar class.

    Use google calendar API. Get and Create events.
    """
    cal_id = 'rdt6sr08t5pddtqn9fk57sd30c@group.calendar.google.com'

    def __init__(self):
        """
        See get_cred in func.
        """
        self.now = date.utcnow().isoformat() + 'Z'

        self.service = get_cred()

    def get_events(self, num: int = 10) -> int:
        """
        Get events, print and return status code.

        :param num: number of events
        :type num: int
        :return: status code
        :rtype: int
        """
        if num < 1:
            return 400
        events_result = self.service.events().list(calendarId=self.cal_id, timeMin=self.now,
                                                   maxResults=num, singleEvents=True,
                                                   orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            return 204
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        return 200

    def create_event(self, data: dict) -> int:
        """
        Create event, print url  and return status code.

        :param data: special dictionary for event formation
        :type data: dict
        :return: status code
        :rtype: int
        """
        if not data:
            return 400
        event = self.service.events().insert(calendarId=self.cal_id, body=data).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        return 200
