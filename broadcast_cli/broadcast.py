# coding=utf-8
import json


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
    def __init__(self, user_id, feeds, content, self_url, created_at):
        self.user_id = user_id
        self.feeds = feeds
        self.content = content
        self.self_url = self_url
        self.created_at = created_at