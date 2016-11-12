# coding=utf-8
from .broadcast import Broadcast


class Actions:
    """
    Performs actions of supplied commands
    """

    def __init__(self, url, auth_token=None):
        self.baseUrl = url.parse(url)
        self.auth_token = auth_token

    def get(self, broadcasts_id: int):
        """
        Get list of Broadcasts or individual one
        :param broadcasts_id:
        :return: Broadcast
        """
        return Broadcast("bil", 'bar')

    def get_all(self):
        return [Broadcast('foo', 'bar'), ]

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
