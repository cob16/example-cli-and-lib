# coding=utf-8
import json

from broadcast_cli.utils import exit_and_fail


class Jsonionise:
    """
    get and set from json
    """

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod  # allows us to initalsie form this
    def from_dict(cls, dict):
        return cls(**dict)


class Broadcast(Jsonionise):
    """
    Python repression of a broadcast obj
    """
    def __init__(self, feed_list, content, created_at=None, id=None, user_id=None, self_url=None):
        self.id = id
        self.user_id = user_id
        self.feed_list = feed_list
        self.content = content
        self.self_url = self_url
        self.created_at = created_at

    @property
    def feed(self):
        return self.feed_list

    @feed.setter
    def feed(self, feed):
        self.feed_list = feed

    # def is_invalid(self): # todo
    #     """
    #     checks to make sure the minimum fields are
    #     """
    #     return self.content is None or self.feed is None:
