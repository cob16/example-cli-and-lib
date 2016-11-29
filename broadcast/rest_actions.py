# coding=utf-8
import json

import requests
from broadcast.broadcast import Broadcast
from furl import furl

from broadcast_cli.utils import exit_and_fail

PREFIX = 'api'
BROADCASTS_URL = '{0}/broadcasts'.format(PREFIX)
SESSION_URL = '{0}/session'.format(PREFIX)

FEEDS = "notification twitter facebook RSS atom email".split()


def raise_for_no_content(reply):
    if reply.status_code == 204:
        exit_and_fail('No content returned from the server')


class RestActions:
    """
    Performs actions of supplied Broadcasts commands
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

    @property
    def url(self):
        return self.base_url.copy()

    def get(self, broadcasts_id: int = None):
        """
        Get list of Broadcasts or individual one
        :param broadcasts_id:
        :return: Broadcast
        """
        if broadcasts_id is None:
            broadcast = self._get(self.url.set(path=BROADCASTS_URL))
        else:
            url_ob = self.url.set(path=BROADCASTS_URL)
            url_ob.path.segments.append(broadcasts_id)
            broadcast = self._get(url_ob)

        if self.return_raw:
            return broadcast.text

        broadcast = broadcast.json()

        if broadcasts_id:
            return Broadcast.from_dict(broadcast)

        return list(
            map((lambda b: Broadcast.from_dict(b)), broadcast))  # convert each broadcast to a Broadcast object to a

    def _get(self, url_ob):
        r = requests.get(url_ob.url, headers={'Authorization': self.auth_token})
        r.raise_for_status()
        RestActions.raise_for_nocontent(r)
        return r

    @staticmethod
    def raise_for_nocontent(r):
        if r.status_code == 204:
            exit_and_fail('No content returned from the server')

    def post(self, broadcast: Broadcast):
        """
        Post Broadcast to server
        """
        data = self._post(broadcast.__dict__, self.url.set(path=BROADCASTS_URL))

        if self.return_raw:
            return data.text

        data = data.json()
        if 'errors' in data:
            exit_and_fail(data['errors'])

        return Broadcast.from_dict(data)

    def _post(self, payload, url, headers=None):
        if headers is None:
            headers = {'Authorization': self.auth_token}

        data = requests.post(url, json=payload, headers=headers)
        data.raise_for_status()
        RestActions.raise_for_nocontent(data)

        return data

    def Authenticate(self, login, password):
        """
        Authenticates with server in order to get auth token
        Sets the current instances auth_token
        :returns: auth_token
        """
        logininfo = dict(login=login, password=password)
        self.auth_token = self._post(logininfo, self.url.set(path=SESSION_URL), headers=False).json()['api_token']
        return self.auth_token
