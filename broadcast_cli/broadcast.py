# coding=utf-8
import json


class Broadcast(object):
    """
    Python repression of a broadcast obj
    """

    def __init__(self, title, body):
        self.title = title
        self.body = body

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod  # allows us to initalsie form this
    def from_json(cls, json_str):
        dict = json.loads(json_str)
        return cls(**dict)
