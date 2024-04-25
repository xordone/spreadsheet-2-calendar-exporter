from datetime import datetime

from dateutil import parser

from classes.generics import Req
from func import payload


class Sheet:
    """
    SpreadSheet Class.

    Use API google spreadsheet. Collects and generates special data for Calendar.
    """
    sheet_id = '1EHVQr3O8N2RG9q53XEY_sg2n23qHrDNVexUbtH6HPy0'
    # sheet_id = '1KM_KGpOeDMTXjKL9Q5-g53W8GDPKM8xNbPQpCpdULMw'
    list_name = 'Август'
    mons = [
            '2019',
            'Января',
            'Февраля',
            'Марта',
            'Апреля',
            'Мая',
            'Июня',
            'Июля',
            'Августа',
            'Сентября',
            'Октября',
            'Ноября',
            'Декабря',
            ]

    def __init__(self):
        """
        See payload in func.
        """
        url = 'https://sheets.googleapis.com/v4/spreadsheets/{0}/values/{1}'.format(self.sheet_id, self.list_name)
        options = payload()
        self.data = Req(url, options)

    def get_data(self):
        """
        Generates a dictionary with special data for the Calendar.

        The data in the tables are not consistent, need to be improved.
        :return: special dict
        :rtype: dict
        """
        cal_data = []
        for i in (self.data.get_json()['values']):
            if len(i) < 2 or not i[0] or not i[0][0].isdigit():
                continue

            if i[2][2] != ':':
                i[2] = '12:34'
            # Собираем строку со временем
            yyyy = int(self.mons[0])
            date_list = i[0].split(' ')
            m = int(self.mons.index(date_list[1].capitalize()))
            d = int(date_list[0])
            h = int(i[2][0:2])
            mm = int(i[2][3:5])
            date_str = '{:%Y-%m-%d %H:%M}'.format(datetime(yyyy, m, d, h, mm))

            date = parser.parse(date_str)
            event = {'start': {
                    'dateTime': date.isoformat(),
                    'timeZone': 'Europe/Moscow',
                    },
                    'end': {
                            'dateTime': date.isoformat(),
                            'timeZone': 'Europe/Moscow',
                            },
                    'summary': i[3],
                    'description': i[6]}
            cal_data.append(event)
        return cal_data
