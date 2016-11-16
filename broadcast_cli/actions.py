# coding=utf-8
import requests
from furl import furl
from requests import HTTPError

from .broadcast import Broadcast
from .utils import exit_and_fail

PREFIX = 'api'
BROADCASTS_URL = '{0}/broadcasts'.format(PREFIX)
USERS_URL = '{0}/users'.format(PREFIX)

FEEDS = "twitter facebook RSS atom email".split()


class Actions:
    """
    Performs actions of supplied commands
    """

    def __init__(self, url, auth_token=None, return_raw=False):
        if furl(url).scheme is '':
            print(url)
            exit_and_fail("URL not valid! Please make sure you included 'https://'")

        self.base_url = furl(url).remove(  # normalise
            args=True,
            path=True,
            username=True,
            password=True
        )
        self.return_raw = return_raw
        self.auth_token = auth_token

    def get(self, broadcasts_id: int = None):
        """
        Get list of Broadcasts or individual one
        :param broadcasts_id:
        :return: Broadcast
        """
        if broadcasts_id is None:
            data = self._get(self._geturl().set(path=BROADCASTS_URL))
        else:
            url_ob = self._geturl().set(path=BROADCASTS_URL)
            url_ob.path.segments.append(broadcasts_id)
            data = self._get(url_ob)

        if self.return_raw:
            return data.text

        return data.json()

    @staticmethod
    def _get(url_ob):
        r = requests.get(url_ob.url, auth=('admin', 'admin'))
        r.raise_for_status()
        if r.status_code == 204:
            exit_and_fail('No content returned from the server')
        return r

    def post(self, broadcast: Broadcast) -> bool:
        """
        post Broadcast server
        """
        pass

        # def patch(self, oldBroadcastObj: Broadcast, newBroadcastObj: Broadcast) -> bool:
        #     """
        #     compare with new supplied object and send defences
        #     """
        #     pass

    def _geturl(self):
        return self.base_url.copy()
