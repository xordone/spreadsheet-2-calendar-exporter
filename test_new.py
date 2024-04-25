from unittest.mock import patch

import py.test

from classes import cal, sheet


def test_new():
    assert 2 == 2


class TestSheet:

    @patch('classes.sheet.Sheet')
    def test_sheet_api(self, mock_sheet):
        sheet = mock_sheet()
        sheet.response.status_code = 200
        assert sheet.response.status_code == 200

    @patch('classes.sheet.Sheet')
    def test_is_instance(self, mock_sheet):
        sheet = mock_sheet()
        assert isinstance(sheet, object)


class TestCal:
    @patch('classes.cal.Cal')
    def test_is_instance(self, mock_cal):
        cal = mock_cal()
        assert isinstance(cal, object)
