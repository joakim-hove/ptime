import json
import os
import requests


class BaseClient(object):
    PTIME_URL = os.environ["PTIME_URL"]
    PTIME_USER = os.environ["PTIME_USER"]

    def __init__(self):
        pass

    def run(self):
        data = self.post_data()
        data["user"] = self.PTIME_USER
        response = requests.post(self.url(), json=data)
        return response

    def post_data(self):
        return {}

    def url(self):
        raise NotImplementedError("Each inherited class must implement the url() method")



class StartClient(BaseClient):

    def __init__(self, argv):
        if len(argv) == 0:
            raise ValueError("Too short")

        self.project_id = argv[0]


    def url(self):
        return "{0}/api/task/start/{1}/".format(self.PTIME_URL, self.project_id)



class StopClient(BaseClient):

    def __init__(self, argv):
        pass

    def url(self):
        return "{0}/api/task/stop/".format(self.PTIME_URL)


class PTimeClient(object):
    commands = {"start" : StartClient,
                "stop" : StopClient }

    def __init__(self, argv):
        if len(argv) == 0:
            raise ValueError("Empty argv vector - invalid")

        cmd = argv[0]
        self.client = self.commands[cmd](argv[1:])


    def run(self):
        return self.client.run()

def get(argv):
    pass
