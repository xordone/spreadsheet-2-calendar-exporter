import requests as r


class Req:
    """Simple request class."""

    error = []

    def __init__(self, url: str, params: dict = None) -> None:
        """

        :param url: site url
        :type url: str
        :param params: key=value dict
        :type params: dict
        """
        try:
            self.req = r.get(url, params)
        except r.exceptions.ConnectionError:
            redirect = 'http://www.python.org'
            self.error.append(('invalid url {0}, redirect to {1}'.format(url, redirect)))
            self.req = r.get(redirect)

    def check_error(self):
        """Print errors if exist"""
        for i in self.error:
            print(i)

    def get_json(self):
        """

        :return: json style dict
        :rtype: dict or False
        """
        if not self.error:
            return self.req.json()
        return False

    def get_status_code(self):
        """

        :return: status of  request
        :rtype: int
        """
        return self.req.status_code

    def get_url(self):
        """

        :return: full request url
        :rtype: str
        """
        return self.req.url

    def ok(self):
        """
        Returns True if :attr:`status_code` is less than 400, False if not.

        :return: status of request
        :rtype: bool
        """
        return self.req.ok
