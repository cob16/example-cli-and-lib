class Action:
    URL = None
    auth_token = None

    def __init__(self, url, auth_token=None):
        self.url = url
        self.auth_token = auth_token

    def get(self, data):
        pass

    def post(self, data):
        pass

    def patch(self, data):
        pass

    def delete(self, data):
        pass
