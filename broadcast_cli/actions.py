# coding=utf-8
import requests
from furl import furl

from .broadcast import Broadcast

BROADCASTS = 'api/broadcasts'


class Actions:
    """
    Performs actions of supplied commands
    """

    def __init__(self, url='http://0.0.0.0:3000/api/broadcasts', auth_token=None):
        self.base_url = furl(url).remove(  # normalise
            args=True,
            path=True,
            username=True,
            password=True
        )

        self.auth_token = auth_token

    def get(self, broadcasts_id: int = None):
        """
        Get list of Broadcasts or individual one
        :param broadcasts_id:
        :return: Broadcast
        """
        if broadcasts_id is None:
            return self._get(self._geturl().set(path=BROADCASTS))

        url_ob = self._geturl().set(path=BROADCASTS)
        url_ob.path.segments.append(broadcasts_id)
        data = self._get(url_ob).json()

        return Broadcast.from_dict(data)

        # return list(map(lambda d: Broadcast().from_json(d), data))

    @staticmethod
    def _get(url_ob):
        r = requests.get(url_ob.url, auth=('admin', 'admin'))
        r.raise_for_status()
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

